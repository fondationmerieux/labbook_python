# LabBook project dependencies
## Front and Back End
| Name                    | Version   | License      | static FE | venv FE | venv BE |
|-------------------------|:---------:|:------------:|:---------:|:-------:|:-------:|
| Python                  | 3.11.11   | PSF          |           |         |         |
| Bootstrap               | 5.2.3     | MIT          | x         |         |         |
| Chart                   | 3.6.0     | MIT          | x         |         |         |
| JQuery                  | 3.6.1     | MIT          | x         |         |         |
| JQuery tablesorter      | 2.31.3    | MIT and GPL  | x         |         |         |
| JQuery UI               | 1.13.2    | MIT          | x         |         |         |
| Moment                  | 2.29.4    | MIT          | x         |         |         |
| pivot                   | 2.23.0    | MIT          | x         |         |         |
| Popper                  | 2.11.0    | MIT          | x         |         |         |
| select2                 | 4.0.13    | MIT          | x         |         |         |
| swagger-ui              | 4.15.5    | Apache 2.0   |           | x       |         |
| Babel                   | 2.18.0    | BSD          |           | x       | x       |
| Flask                   | 3.1.3     | BSD          |           | x       | x       |
| Flask-Babel             | 4.0.0     | BSD          |           | x       | x       |
| Jinja2                  | 3.1.6     | BSD          |           | x       | x       |
| gunicorn                | 26.2.0    | MIT          |           | x       | x       |
| pip                     | 25.2.0    | MIT          |           | x       | x       |
| pipenv                  | 2025.0.1  | MIT          |           | x       | x       |
| requests                | 2.34.2    | Apache 2.0   |           | x       | x       |
| urllib3                 | 2.7.0     | MIT          |           | x       |         |
| pip-audit               | 2.10.1    | Apache 2.0   |           | x       | x       |
| tomli                   | 2.4.1     | MIT          |           | x       | x       |
| Werkzeug                | 3.1.8     | BSD          |           | x       | x       |
| alembic                 | 1.19.1    | MIT          |           |         | x       |
| Flask-RESTful           | 0.3.10    | BSD          |           |         | x       |
| hl7apy                  | 1.3.5     | MIT          |           |         | x       |
| mysql-connector-python  | 8.0.32    | GPL 2        |           |         | x       |
| pdfkit                  | 1.0.0     | MIT          |           |         | x       |
| pikepdf                 | 10.12.0   | MPL 2.0      |           |         | x       |
| Pillow                  | 12.3.0    | HPND         |           |         | x       |
| python-barcode          | 0.16.1    | MIT          |           |         | x       |
| qrcode                  | 8.2.0     | BSD          |           |         | x       |
| relatorio               | 1.0.0     | GPL          |           |         | x       |
| reportlab               | 5.0.1     | BSD          |           |         | x       |
| bcrypt                  | 5.0.0     | Apache 2.0   |           |         | x       |
| authlib                 | 1.7.2     | BSD          |           |         | x       |
| Flask-Cors              | 6.0.5     | MIT          |           |         | x       |
| mailjet-rest            | 1.8.0     | MIT          |           |         | x       |

> Note :
>
> - static FE = file are located at path labbook_FE/app/static/vendor/
> - venv FE = major library installed in python virtual environment of labbook front end via pip install command
> - venv BE = major library installed in python virtual environment of labbook back end via pip install command
> - python-barcode and Pillow are related
> - See Pipfile files for each project 
