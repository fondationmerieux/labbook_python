# -*- coding:utf-8 -*-
import os
import logging
import tomli

from app.models.Constants import Constants
from app.models.Logs import Logs


class Form:
    log = logging.getLogger('log_front')

    html_content = ''
    html_var = ''
    json_var = {}

    @staticmethod
    def build_form(type_form, filename, lang='fr'):
        dirpath = Constants.cst_form_pat

        path = os.path.join(dirpath, filename)

        Form.html_content = ''
        Form.html_var = ''
        Form.json_var = { 'id_user': 'id_user'}

        l_obj_html = {}

        # Test if file exist
        if os.path.isfile(path) and path.endswith('.toml'):
            Form.log.info(Logs.fileline() + ' : build_form file exist')

            with open(path, "rb") as f:
                form_toml = tomli.load(f)

            # Form.log.error(Logs.fileline() + " : DEBUG toml = " + str(form_toml))

            # --- BUILD HTML OBJECT ---
            for elem in form_toml['description']['form_element']:
                # Form.log.info(Logs.fileline() + ' : DEBUG elem = ' + str(elem))
                # predefined case
                if elem and 'labbook_ref' in elem:
                    # Form.log.info(Logs.fileline() + ' : DEBUG TODO labbook_ref')

                    l_attr   = []
                    required = False

                    for key in elem:
                        if key.startswith('attr_'):
                            if key == 'attr_value':
                                value = elem[key]
                            else:
                                attr_name  = key.replace('attr_', '')
                                attr_value = elem[key]
                                attr_pair  = f'{attr_name}={attr_value}'

                                if attr_name == "required":
                                    required = True

                                l_attr.append(attr_pair)

                    l_obj_html[elem['labbook_ref']] = Form.build_labbook_elem(elem['labbook_ref'], l_attr)

                    if 'input_type' in elem:
                        Form.build_js_data(elem['labbook_ref'], elem['input_type'], required)
                    elif elem['labbook_ref'] == 'pat_code':
                        Form.build_js_data(elem['labbook_ref'], 'text_special', required)
                # new case
                elif elem and 'id' in elem:
                    # input element
                    if 'input_type' in elem:
                        # Form.log.info(Logs.fileline() + ' : DEBUG TODO input_type')
                        value     = ''
                        l_options = []
                        l_attr    = []
                        required  = False

                        if 'options' in elem:
                            l_options = elem['options']

                        for key in elem:
                            if key.startswith('attr_'):
                                if key == 'attr_value':
                                    value = elem[key]
                                else:
                                    attr_name  = key.replace('attr_', '')
                                    attr_value = elem[key]
                                    attr_pair  = f'{attr_name}={attr_value}'

                                    if attr_name == "required":
                                        required = True

                                    l_attr.append(attr_pair)

                        # Form.log.info(Logs.fileline() + ' : DEBUG l_attr = ' + str(l_attr))

                        l_obj_html[elem['id']] = Form.build_input_elem(elem['input_type'], elem['id'], elem['label'], value, l_options, l_attr)

                        Form.build_js_data(elem['id'], elem['input_type'], required)

                    # cosmetics only
                    elif 'type' in elem:
                        l_obj_html[elem['id']] = Form.build_simple_elem(elem['type'], elem['id'], elem['label'])
                    else:
                        Form.log.error(Logs.fileline() + ' : Missing input_type or type for this form_element : ' + str(elem))
                        Form.html_content += ' Missing input_type or type for this form_element : ' + str(elem)
                        return Form.html_content
                else:
                    Form.log.error(Logs.fileline() + ' : Missing labbook_ref or id for this form_element : ' + str(elem))
                    Form.html_content += 'Missing labbok_ref or id for this form_element : ' + str(elem)
                    return Form.html_content

            # --- LAYOUT OF ELEMENTS ---
            Form.read_layout(form_toml['layout']['rows'], l_obj_html)

            # Form.log.info(Logs.fileline() + ' : DEBUG html_content = ' + str(Form.html_content))

            # Form.json_var = json.dumps(Form.json_var)
            Form.json_var = '{' + ', '.join(f'"{key}": {value}' for key, value in Form.json_var.items()) + '}'

            # Form.log.info(Logs.fileline() + ' : DEBUG json_var = ' + str(Form.json_var))

        Form.log.info(Logs.fileline())

        obj = {}

        obj['form_html'] = Form.html_content
        obj['json_save'] = Form.html_var + '\nvar param = ' + Form.json_var

        return obj

    @staticmethod
    def build_simple_elem(type, id, label):
        from flask_babel import gettext as _

        elem = ''
        label = _(label)

        if type in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            elem = '<' + type + ' id="' + str(id) + '" class="fw-bold">' + str(label) + '</' + type + '>'
        else:
            elem = '<' + type + ' id="' + str(id) + '" class="mt-2">' + str(label) + '</' + type + '>'

        return elem

    @staticmethod
    def build_labbook_elem(id, l_attr=[]):
        elem = ''

        if id in ('pat_ano', 'pat_code_lab', 'pat_code', 'pat_name', 'pat_midname', 'pat_maiden', 'pat_firstname',
                  'pat_sex', 'pat_birth', 'pat_birth_approx', 'pat_age', 'pat_age_unit', 'pat_nationality', 'pat_resident',
                  'pat_blood_group', 'pat_blood_rhesus', 'pat_address', 'pat_phone1', 'pat_phone2', 'pat_profession',
                  'search_zipcity', 'pat_pbox', 'pat_district', 'pat_zipcode', 'pat_city', 'pat_email'):
            elem = '{% include "elem/' + id + '.html" %}'

        if l_attr:
            elem = ('{% with l_attr=' + str(l_attr) + ' %}' + elem + '{% endwith %}')

        return elem

    @staticmethod
    def build_input_elem(type, id, label, value='', l_options=[], l_attr=[]):
        elem = ''

        if type == 'select':
            elem = ('{% with id="' + str(id) + '", label="' + str(label) + '", l_options=' + str(l_options) + ', value=args[\'' + str(id) + '\'] %}'
                    '{% include "elem/basic_select.html" %}'
                    '{% endwith %}')
        if type == 'radio':
            elem = ('{% with id="' + str(id) + '", label="' + str(label) + '", l_options=' + str(l_options) + ', value=args[\'' + str(id) + '\'] %}'
                    '{% include "elem/basic_radio.html" %}'
                    '{% endwith %}')
        elif type == 'text':
            elem = ('{% with id="' + str(id) + '", label="' + str(label) + '", value="' + value + '", l_attr=' + str(l_attr) + ', value=args[\'' + str(id) + '\'] %}'
                    '{% include "elem/basic_text.html" %}'
                    '{% endwith %}')
        elif type == 'textarea':
            elem = ('{% with id="' + str(id) + '", label="' + str(label) + '", value="' + value + '", l_attr=' + str(l_attr) + ', value=args[\"' + str(id) + '\"] %}'
                    '{% include "elem/basic_textarea.html" %}'
                    '{% endwith %}')
        elif type == 'number':
            elem = ('{% with id="' + str(id) + '", label="' + str(label) + '", value="' + value + '", l_attr=' + str(l_attr) + ', value=args[\'' + str(id) + '\'] %}'
                    '{% include "elem/basic_number.html" %}'
                    '{% endwith %}')
        elif type == 'date':
            elem = ('{% with id="' + str(id) + '", label="' + str(label) + '", value="' + value + '", l_attr=' + str(l_attr) + ', value=args[\'' + str(id) + '\'] %}'
                    '{% include "elem/basic_date.html" %}'
                    '{% endwith %}')
        elif type == 'datetime-local':
            elem = ('{% with id="' + str(id) + '", label="' + str(label) + '", value="' + value + '", l_attr=' + str(l_attr) + ', value=args[\'' + str(id) + '\'] %}'
                    '{% include "elem/basic_datetime.html" %}'
                    '{% endwith %}')

        return elem

    @staticmethod
    def open_div(l_class=''):

        if l_class == '':
            elem = '<div>'
        else:
            elem = ('<div class="' + l_class + '">')

        return elem

    @staticmethod
    def build_div_obj(id, obj_html, l_class=''):
        elem = ('<div id="div_' + id + '" class="form-group d-md-flex mt-1 my-md-2 ' + l_class + '">' + obj_html + '</div>')

        return elem

    @staticmethod
    def read_layout(data, l_obj_html):
        for item in data:
            l_class = ''

            # Form.log.info(Logs.fileline() + ' : DEBUG read_layout data = ' + str(item))

            if isinstance(item, (dict, list)) and 'class' in item:
                l_class = item['class']

            Form.html_content += Form.open_div(l_class)

            if 'cols' in item:
                Form.read_layout(item['cols'], l_obj_html)
                Form.html_content += '</div><!-- close cols -->'
            elif isinstance(item, (dict, list)) and 'elements' in item:
                Form.read_layout(item['elements'], l_obj_html)
                Form.html_content += '</div><!-- close elements -->'
            elif isinstance(item, (dict, list)) and 'element' in item:
                name_obj_html = item['element']

                Form.html_content += Form.build_div_obj(name_obj_html, l_obj_html[name_obj_html], l_class)
                Form.html_content += '</div><!-- close element -->'

    @staticmethod
    def build_js_data(id, type, required):
        if type in ('text', 'number', 'date', 'datetime-local', 'select'):
            Form.html_var += 'var ' + str(id) + ' = $("#' + str(id) + '").val() ;\n'

            if id in ('pat_phone1', 'pat_phone2'):
                Form.html_var += str(id) + ' = ' + str(id) + '.replaceAll(" ", "") ;\n'
        elif type in ('radio'):
            Form.html_var += 'var ' + str(id) + ' = $("input:radio[name=' + str(id) + ']:checked").val() ;\n'
        elif type in ('textarea'):
            Form.html_var += 'var ' + str(id) + ' = $.trim( $("#' + str(id) + '").val() ) ;\n'
        elif type in ('text_special'):
            Form.html_var += 'var ' + str(id) + ' = $("#' + str(id) + '").text() ;\n'

        Form.json_var[str(id)] = str(id)

        if required:
            # test if value is not empty and elements and parents are displayed
            Form.html_var += ('if (' + str(id) + ' === "" && !($("#' + str(id) + '").closest(":hidden").length > 0))\n'
                              '{\n'
                              '$("#' + str(id) + '").addClass("is-invalid");\n'
                              'alert("{{ _("Veuillez saisir les champs obligatoires (*)") }}");\n'
                              'return;\n'
                              '}\n')
