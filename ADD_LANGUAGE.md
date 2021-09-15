TODO FINISH WRITING THIS DOCUMENT


To add a new language in Labbook

In Labbook_FE/app/__init__.py file

Add code of language to this dict
LANGUAGES = {
    'fr_FR': 'French',
    ...
    }

Do the same in labbook_BE/app/__init__.py file

In Labbook_FE/app/__init__.py file add case in locale() function  

In virtual of labbook_FE and labbook_BE

For each new language (exemple with french and arabic)
pybabel init -i translations/messages.pot -d translations/ -l fr_FR
pybabel init -i translations/messages.pot -d translations/ -l ar

Fill the new file(s)

pybabel compile -d translations/
