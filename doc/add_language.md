# Adding a language to LabBook

There are two kinds of addition, and the work is not the same.

**Interface only.** The screens, the buttons and the reports speak the new language, but what
the laboratory typed into the database stays as it was entered. Arabic, Khmer, Laotian,
Malagasy and Spanish are in that case.

**Interface and database.** The same, plus the analysis names, the variable names and the
dictionaries, which are translated too. Only English and Portuguese are in that case today.

Start with the interface: the second part builds on it and cannot be done first.

## Interface

### 1. Declare the language

Four places, none of which can be skipped.

`labbook_FE/app/__init__.py`, the list of accepted locales:

```python
LANGUAGES = {
    'fr_FR': 'French',
    ...
    'pt': 'Portuguese',
}
```

The same list, identically, in `labbook_BE/app/__init__.py`.

`labbook_FE/app/__init__.py` again, two side tables that follow it:

```python
LANG_SELECT = {..., 'pt': 'PT'}          # the code shown in the top bar
EU_FORMAT_LANGS = {..., 'pt'}            # add it here for a day/month/year date
```

A locale left out of `EU_FORMAT_LANGS` gets the month/day/year format, which is what English (US)
needs.

`labbook_FE/app/templates/menu-country.html`, the language picker of the header. The file is
included by `skeleton.html`, so the entry shows on every screen:

```html
<li>
    <a class="dropdown-item" href="{{ session['server_ext'] }}/lang/pt">{{ _("Portugais (PT)") }}</a>
</li>
```

`labbook_FE/app/templates/setting-pref.html`, the `pref_lang_pdf` dropdown, which sets the
language of the reports. Every language belongs there:

```html
<option value="pt" {% if args['pref_list'] and args['pref_list'][14]['value'] == "pt" %} selected {% endif %}>{{ _("Portugais") }}</option>
```

The same screen holds a second dropdown, `pref_lang_db`, the language of the referential. That
one is for major languages only, see below.

### 2. Create the catalogue

Once in `labbook_FE`, once in `labbook_BE`: the two applications hold separate catalogues and
separate `babel.cfg` files. From the virtual environment of the application:

```bash
pybabel extract -F babel.cfg -o translations/messages.pot .
pybabel init -i translations/messages.pot -d translations/ -l pt
```

`init` is for a new language only. An existing one is refreshed with:

```bash
pybabel update --no-fuzzy-matching -i translations/messages.pot -d translations/
```

`--no-fuzzy-matching` matters: without it pybabel copies translations between strings that
merely look alike.

### 3. Translate and compile

Fill `translations/pt/LC_MESSAGES/messages.po`, then, in each of the two applications:

```bash
pybabel compile -d translations/
```

The French strings are the keys, so an untranslated entry shows in French rather than breaking.

At this point the interface is done. Restart and check the language picker.

## Database strings

Analysis names, variable names and dictionary entries live in the database, not in the code, so
pybabel cannot find them by reading the source.

### What `messages_pybabel.py` is for

`app/translations/messages_pybabel.py` exists only to make those strings visible to pybabel. It
holds nothing but a long list of calls:

```python
_("abondance")
_("absent")
_("baar")
```

None of it is ever executed. The extraction reads the file, the strings land in
`messages.pot`, and they are translated in the `.po` like any other. A string that is in the
database but missing from this file will never be translated: when a laboratory adds analyses
of its own, they have to be added here.

### Filling the translations table

Once the catalogue is compiled, `Various.updateTranslationsTable(locale)` walks the analyses,
the variables and the dictionaries, translates each name through the catalogue, and writes the
result into the `translations` table:

| Column | Content |
|---|---|
| `tra_lang` | the locale, `pt` for instance |
| `tra_type` | `ana_name`, `var_name` or `dico_name` |
| `tra_ref` | identifier of the row being translated |
| `tra_text` | the translated text |

A row already present is left alone, so the operation can be replayed.

### Declaring the language as a major one

The list of locales that get this treatment is written in the code, in
`labbook_BE/app/services/GeneralRest.py`, class `InitVersion`:

```python
locales = ['en_GB', 'pt']  # add Portuguese
```

Adding a locale here is what makes a language a major one. Without it the interface is
translated and the database is not.

The screen has to follow: the `pref_lang_db` dropdown of `setting-pref.html` holds the same
list, and it is what lets the laboratory pick the language of its referential.

```html
<option value="pt" {% if args['pref_list'] and args['pref_list'][15]['value'] == "pt" %} selected {% endif %}>{{ _("Portugais") }}</option>
```

`InitVersion` runs once, on the first call after an installation or an update, and clears its
own flag afterwards. To replay it on an existing installation, the `ini_stat` flag of the
version row has to be set back to `Y`.

## Checklist

| Step | Interface only | Also the database |
|---|---|---|
| `LANGUAGES` in the two `__init__.py` | yes | yes |
| `LANG_SELECT` and `EU_FORMAT_LANGS` | yes | yes |
| entry in the header picker, `menu-country.html` | yes | yes |
| entry in the `pref_lang_pdf` dropdown | yes | yes |
| `pybabel init` then `compile`, in the two applications | yes | yes |
| strings present in `messages_pybabel.py` | no | yes |
| locale added in `GeneralRest.py` | no | yes |
| entry in the `pref_lang_db` dropdown | no | yes |
| `ini_stat` reset to replay the filling | no | yes, on an existing installation |
