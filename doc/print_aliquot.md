# Printing aliquot tube labels

LabBook does not format labels. It runs a script and hands it the values of the aliquot, and
the script decides what to print and where to send it. Neither the printer model nor the label
layout has to be known by LabBook.

The printer must be reachable over the network. See the last section for why a printer plugged
into the server cannot be used.

## How it works

The printers are declared in the settings, screen `list-printer`. A printer holds a name and
the file name of its script.

The script is uploaded from that same screen, button `Importer un script d'impression`. Only
`.sh` files are accepted and they land in `/storage/resource/printer/`. The name entered on the
printer itself must match the name of the uploaded file.

When the operator prints an aliquot from the storage screen, LabBook runs:

    sh /storage/resource/printer/<script of the chosen printer>

with the values of that aliquot set as environment variables. The output of the script, its
error messages included, is written to `/storage/io/print.out`, overwritten at every print.

## Values the script receives

Every variable is always set. A value the record does not hold arrives as an empty string, so
the script never has to test whether a variable exists. Dates are written as `DD/MM/YYYY`.

| Variable | Content |
|---|---|
| `PRINT_ALIQUOT_ID` | aliquot number |
| `PRINT_ALIQUOT_DATE` | date the aliquot was stored |
| `PRINT_PATHOGEN` | pathogen |
| `PRINT_SAMPLE_TYPE` | specimen type |
| `PRINT_PATIENT_CODE` | patient code |
| `PRINT_PATIENT_LAB_CODE` | laboratory code of the patient |
| `PRINT_PATIENT_NAME` | family name |
| `PRINT_PATIENT_FIRSTNAME` | given name |
| `PRINT_RECORD_NUMBER` | record number |
| `PRINT_RECORD_INTERNAL_NUMBER` | internal record number |
| `PRINT_PRESCRIPTION_DATE` | prescription date |
| `PRINT_TEST_CODE` | analysis code |
| `PRINT_TEST_NAME` | analysis name |
| `PRINT_TEST_LOINC` | LOINC code of the analysis |
| `PRINT_STORAGE_ROOM` | room |
| `PRINT_STORAGE_CHAMBER` | chamber |
| `PRINT_STORAGE_COMPARTMENT` | compartment |
| `PRINT_STORAGE_BOX` | box |
| `PRINT_STORAGE_POSITION` | position inside the box |

## Example, ZPL over the network

Most label printers listen on port 9100 and accept ZPL, which is plain text. Nothing has to be
installed: the shell opens the connection itself.

```sh
#!/bin/sh
# Aliquot tube label, sent as ZPL to a network printer.

PRINTER_IP=192.168.1.50
PRINTER_PORT=9100

cat > /dev/tcp/$PRINTER_IP/$PRINTER_PORT <<END
^XA
^CI28
^FO20,20^A0N,28^FD${PRINT_PATIENT_NAME} ${PRINT_PATIENT_FIRSTNAME}^FS
^FO20,55^A0N,24^FD${PRINT_TEST_CODE}  ${PRINT_ALIQUOT_DATE}^FS
^FO20,90^BCN,50,Y^FD${PRINT_ALIQUOT_ID}^FS
^FO20,165^A0N,22^FD${PRINT_STORAGE_BOX} / ${PRINT_STORAGE_POSITION}^FS
^XZ
END
```

`^CI28` selects UTF-8: without it the printer drops accented characters. `^FO x,y` places a
block, in dots, about 8 per millimetre. `^BCN,50,Y` draws the barcode, `50` being its height
and `Y` printing the number under the bars.

## Printers attached to the server are not supported

LabBook runs inside a container, which does not see a printer plugged into the machine hosting
it. Reaching one would mean opening a connection to the host, or running a second component
there, and neither belongs to LabBook: the script is managed from LabBook and lives in its
storage.

The printer must therefore be reachable over the network. Every label printer offers an
Ethernet or Wi-Fi option, so this is a purchase requirement rather than a technical limit.

## Rules for the script author

- Quote the variables, `"$PRINT_PATIENT_NAME"` and not `$PRINT_PATIENT_NAME`, otherwise a name
  holding a space is cut in two.
- Return 0 when the label was sent, anything else on failure.
- Write the reason of a failure on the standard output, it lands in `/storage/io/print.out`.
