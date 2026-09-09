# -*- coding:utf-8 -*-
import sys
import ast
import getopt
import json
import os
import subprocess

from relatorio.templates.opendocument import Template

TMP_DIR = '/home/apps/labbook_BE/labbook_BE/tmp/'

# Pdf.py drops the data of every generated report here, as a Python repr
DATA_DUMP = '/storage/resource/template/data_template_report'


def load_data(data_path, verbose=False):
    """Read the data file: the Python repr written by Pdf.py, or plain JSON."""
    with open(data_path, "r", encoding="utf-8") as file_data:
        raw = file_data.read()

    # Pdf.py writes str(data), which json cannot read: bytes for the logo,
    # single quotes, Python None. ast reads it as it is written.
    try:
        data = ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        data = json.loads(raw)

    if verbose:
        print('data keys = ' + str(sorted(data)))

    return data


def genere_pdf(data_path, template, pdf, verbose=False):
    tmp_odt = os.path.join(TMP_DIR, pdf)
    out_pdf = os.path.join(TMP_DIR, pdf + '.pdf')

    for label, path in (('data', data_path), ('template', template)):
        if not os.path.isfile(path):
            print('%s file not found: %s' % (label, path))
            return False

    if verbose:
        print('data     = ' + data_path)
        print('template = ' + template)
        print('tmp_odt  = ' + tmp_odt)
        print('out_pdf  = ' + out_pdf)

    # read file data
    try:
        data = load_data(data_path, verbose)
    except Exception as err:
        print('read file data failed, err=' + str(err) + ', data_path=' + str(data_path))
        return False

    # write odt with data and template
    try:
        tpl = Template(source="", filepath=template)

        with open(tmp_odt, "wb") as f:
            f.write(tpl.generate(o=data).render().getvalue())
    except Exception as err:
        print('write odt with data and template failed, err=' + str(err) + ', template=' + str(template))
        return False

    # convert odt to pdf via unoserver
    # a list, not a shell line: a file name can never extend the command
    argv = ["unoconvert", "--convert-to", "pdf",
            "--input-filter", "writer8",
            "--filter-option", "SelectPdfVersion=1",
            tmp_odt, out_pdf]

    if verbose:
        print('convert argv = ' + str(argv))

    try:
        result = subprocess.run(argv, capture_output=True, text=True, check=False)  # nosec B603
    except Exception as err:
        print('convert odt to PDF failed, err=' + str(err) + ', template=' + str(template))
        return False

    if result.returncode != 0:
        print('unoconvert returned %d' % result.returncode)
        print(result.stdout.strip())
        print(result.stderr.strip())
        return False

    if not os.path.isfile(out_pdf) or os.path.getsize(out_pdf) == 0:
        print('no PDF produced: ' + out_pdf)
        return False

    print('PDF written: %s (%d bytes)' % (out_pdf, os.path.getsize(out_pdf)))

    return True


def usage():
    print("Usage : %s [-h|--help] [-v|--verbose] [-d|--data path_data] [-t|--template path_template] [-p|--pdf name_pdf]" % sys.argv[0])
    print("   -h : help")
    print("   -d : path of data input, default " + DATA_DUMP)
    print("   -t : path of template input (.odt)")
    print("   -p : name of PDF output without .pdf, written under " + TMP_DIR)
    print("   -v : verbose mode")
    print("")
    print("The data file is the one Pdf.py writes on every generated report.")
    print("Generate one report from the GUI, then iterate on the template here.")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvd:t:p:", ["help", "verbose", "data=", "template=", "pdf="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    verbose  = False
    data     = DATA_DUMP
    template = ""
    pdf      = ""

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-d", "--data"):
            data = str(arg).strip()
        elif opt in ("-t", "--template"):
            template = str(arg).strip()
        elif opt in ("-p", "--pdf"):
            pdf = str(arg).strip()
        else:
            usage()
            sys.exit(2)

    if not template or not pdf:
        print("-t and -p are required")
        usage()
        sys.exit(2)

    sys.exit(0 if genere_pdf(data, template, pdf, verbose) else 1)


if __name__ == "__main__":
    main()
