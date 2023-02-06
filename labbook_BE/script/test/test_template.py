# -*- coding:utf-8 -*-
import sys
import getopt
import locale
import os
import json

from relatorio.templates.opendocument import Template

# locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')


def genere_pdf(data, template, pdf, verbose=False):
    ret_sc = True

    tmp_odt = os.path.join('/home/apps/labbook_BE/labbook_BE/tmp/', pdf)
    out_pdf = os.path.join('/home/apps/labbook_BE/labbook_BE/tmp/', pdf + '.pdf')

    print('path tmp_odt = ' + str(tmp_odt))
    print('path out_pdf = ' + str(out_pdf))

    # read file data
    try:
        data_path = data

        print('path data_path = ' + str(data_path))

        file_data = open(data_path, "r", encoding="utf-8")
        data = file_data.read()

        print('data raw = ' + str(data))

        data = json.loads(data)
        
        print('data json = ' + str(data))
    except Exception as err:
        print('read file data, failed, err=' + str(err) + ', data_path=' + str(data_path))
        return False

    # write odt with data and template
    try:
        tpl_path = template

        print('path tpl_path = ' + str(tpl_path))

        tpl = Template(source="", filepath=tpl_path)

        f = open(tmp_odt, "wb")
        f.write(tpl.generate(o=data).render().getvalue())
    except Exception as err:
        print('write odt with data and template, failed, err=' + str(err) + ', template=' + str(template) + ', pdf=' + str(pdf))
        return False

    # convert odt to pdf via openoffice
    try:
        cmd = ('unoconv -e SelectPdfVersion=1 -f pdf -o ' + out_pdf + ' ' + tmp_odt + ' > ' + '/home/apps/labbook_BE/labbook_BE/tmp/' + 'unoconv.out 2>&1')

        print('convert odt to pdf cmd=' + cmd)
        os.system(cmd)

        file_exists = os.path.exists(out_pdf + '.pdf')

        # if file ends by .pdf remove it
        if file_exists:
            print('remove .pdf from ' + out_pdf + '.pdf')
            import shutil

            shutil.move(out_pdf + '.pdf', out_pdf)
    except Exception as err:
        print('convert odt to PDF failed, err=' + str(err) + ', template=' + str(template) + ', pdf=' + str(pdf))
        return False

    return ret_sc


def usage():
    print("Usage : %s [-h|--help] [-v|--verbose] [-d|--data path_data] [-t|--template path_template] [-p|--pdf path_pdf]" % sys.argv[0])
    print("   -h : help")
    print("   -t : path of data input")
    print("   -t : path of template input")
    print("   -p : name of PDF output without .pdf")
    print("   -v : verbose mode")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvd:t:p:", ["help", "verbose", "data=", "template=", "pdf="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    verbose  = False
    statut   = 1
    data     = ""
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

    if genere_pdf(data, template, pdf, verbose):
        statut = 0

    sys.exit(statut)


if __name__ == "__main__":
    main()
