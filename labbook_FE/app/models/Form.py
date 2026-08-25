# -*- coding:utf-8 -*-
import os
import logging
import tomli

from app.models.Constants import Constants
from app.models.Logs import Logs


class Form:
    # Logger for frontend form generation
    log = logging.getLogger('log_front')

    # Accumulate HTML, JS and JSON variables while building the form
    html_content = ''
    html_var = ''
    json_var = {}

    @staticmethod
    def build_form(type_form, filename, lang='fr'):
        """
        Main entry point.
        - Load TOML file describing the form.
        - Build HTML widgets from TOML description.
        - Build JS variables used to save the form.
        - Build history tables + JS if 'history' section is present.
        """
        dirpath = Constants.cst_form_pat

        path = os.path.join(dirpath, filename)
        Form.html_content = ''
        Form.html_var = ''
        # json_var is used to build the 'param' object in the JS save function
        Form.json_var = {'id_user': 'id_user'}

        l_obj_html = {}
        history_js = ''

        # Check that the TOML file exists and has the expected extension
        if os.path.isfile(path) and path.endswith('.toml'):
            Form.log.info(Logs.fileline() + ' : build_form file exist')

            with open(path, "rb") as f:
                form_toml = tomli.load(f)

            # Form.log.error(Logs.fileline() + " : DEBUG toml = " + str(form_toml))

            # --- BUILD HTML OBJECTS FROM DESCRIPTION ---
            for elem in form_toml['description']['form_element']:
                # Case 1: predefined LabBook element (labbook_ref refers to an existing include)
                if elem and 'labbook_ref' in elem:
                    l_attr = []
                    required = False

                    # Collect all attributes, detect "required"
                    for key in elem:
                        # attr_value holds the default value of the element, handled elsewhere
                        if key.startswith('attr_') and key != 'attr_value':
                            attr_name = key.replace('attr_', '')
                            attr_value = elem[key]
                            attr_pair = f'{attr_name}={attr_value}'
                            if attr_name == "required":
                                required = True
                            l_attr.append(attr_pair)

                    # Include the corresponding HTML template (patient fields, etc.)
                    l_obj_html[elem['labbook_ref']] = Form.build_labbook_elem(elem['labbook_ref'], l_attr)

                    # Build JS read/validation for this field if needed
                    if 'input_type' in elem:
                        Form.build_js_data(elem['labbook_ref'], elem['input_type'], required)
                    elif elem['labbook_ref'] == 'pat_code':
                        # Special case: pat_code is read as text content
                        Form.build_js_data(elem['labbook_ref'], 'text_special', required)

                # Case 2: generic new element defined by an explicit "id"
                elif elem and 'id' in elem:
                    # Input element with a real input_type
                    if 'input_type' in elem:
                        value = ''
                        l_options = []
                        l_attr = []
                        required = False

                        if 'options' in elem:
                            l_options = elem['options']

                        # Collect attributes for this element, detect "required"
                        for key in elem:
                            if key.startswith('attr_'):
                                if key == 'attr_value':
                                    value = elem[key]
                                else:
                                    attr_name = key.replace('attr_', '')
                                    attr_value = elem[key]
                                    attr_pair = f'{attr_name}={attr_value}'
                                    if attr_name == "required":
                                        required = True
                                    l_attr.append(attr_pair)

                        # Build HTML for this input element (select, text, textarea, etc.)
                        l_obj_html[elem['id']] = Form.build_input_elem(
                            elem['input_type'],
                            elem['id'],
                            elem['label'],
                            value,
                            l_options,
                            l_attr
                        )

                        # Prepare JS to read/validate this field when saving
                        Form.build_js_data(elem['id'], elem['input_type'], required)

                    # Case 3: cosmetic element only (title, paragraph, separators, etc.)
                    elif 'type' in elem:
                        l_obj_html[elem['id']] = Form.build_simple_elem(
                            elem['type'],
                            elem['id'],
                            elem['label']
                        )
                    else:
                        # Invalid configuration for this element: missing input_type/type
                        Form.log.error(Logs.fileline() + ' : Missing input_type or type for this form_element : ' + str(elem))
                        Form.html_content += ' Missing input_type or type for this form_element : ' + str(elem)
                        return Form.html_content

                else:
                    # Invalid configuration: no labbook_ref and no id
                    Form.log.error(Logs.fileline() + ' : Missing labbook_ref or id for this form_element : ' + str(elem))
                    Form.html_content += 'Missing labbok_ref or id for this form_element : ' + str(elem)
                    return Form.html_content

            # --- Build history tables containers and JS using history config ---
            history_js = Form.build_history(form_toml, l_obj_html)

            # --- LAYOUT OF ELEMENTS (ROWS / COLS / ELEMENTS) ---
            Form.read_layout(form_toml['layout']['rows'], l_obj_html)

            # Form.log.info(Logs.fileline() + ' : DEBUG html_content = ' + str(Form.html_content))

            # Build JSON-like part used in JS: var param = { "field": field, ... }
            Form.json_var = '{' + ', '.join(f'"{key}": {value}' for key, value in Form.json_var.items()) + '}'

            # Form.log.info(Logs.fileline() + ' : DEBUG json_var = ' + str(Form.json_var))

        Form.log.info(Logs.fileline())

        obj = {}

        # HTML to inject in the template
        obj['form_html'] = Form.html_content
        # JS variables used on patient form save
        obj['json_save'] = Form.html_var + '\nvar param = ' + Form.json_var
        # JS related to history tables (list + save + delete)
        obj['history_js'] = history_js

        return obj

    @staticmethod
    def build_simple_elem(type, id, label):
        """
        Build simple cosmetic elements (titles, static text, etc.).
        """
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
        """
        Build predefined LabBook patient elements by including existing templates.
        l_attr is passed through Jinja "with" to customize attributes.
        """
        elem = ''

        if id in ('pat_ano', 'pat_code_lab', 'pat_code', 'pat_name', 'pat_midname', 'pat_maiden', 'pat_firstname',
                  'pat_sex', 'pat_birth', 'pat_birth_approx', 'pat_age', 'pat_age_unit', 'pat_nationality', 'pat_resident',
                  'pat_blood_group', 'pat_blood_rhesus', 'pat_address', 'pat_phone1', 'pat_phone2', 'pat_profession',
                  'search_zipcity', 'pat_pbox', 'pat_district', 'pat_zipcode', 'pat_city', 'pat_email'):
            elem = '{% include "elem/' + id + '.html" %}'

        if l_attr:
            # Inject l_attr as Jinja context for the included template
            elem = ('{% with l_attr=' + str(l_attr) + ' %}' + elem + '{% endwith %}')

        return elem

    @staticmethod
    def build_input_elem(type, id, label, value='', l_options=[], l_attr=[]):
        """
        Build HTML for generic input elements (select, radio, text, textarea, number, date, datetime-local).
        The HTML is a Jinja "with" block including the correct template.
        """
        elem = ''

        if type == 'select':
            elem = (
                '{% with id="' + str(id) + '", label="' + str(label) +
                '", l_options=' + str(l_options) +
                ', value=args[\'' + str(id) + '\'] %}'
                '{% include "elem/basic_select.html" %}'
                '{% endwith %}'
            )
        elif type == 'radio':
            elem = (
                '{% with id="' + str(id) + '", label="' + str(label) +
                '", l_options=' + str(l_options) +
                ', value=args[\'' + str(id) + '\'] %}'
                '{% include "elem/basic_radio.html" %}'
                '{% endwith %}'
            )
        elif type == 'text':
            elem = (
                '{% with id="' + str(id) + '", label="' + str(label) +
                '", value="' + value + '", l_attr=' + str(l_attr) +
                ', value=args[\'' + str(id) + '\'] %}'
                '{% include "elem/basic_text.html" %}'
                '{% endwith %}'
            )
        elif type == 'textarea':
            elem = (
                '{% with id="' + str(id) + '", label="' + str(label) +
                '", value="' + value + '", l_attr=' + str(l_attr) +
                ', value=args["' + str(id) + '"] %}'
                '{% include "elem/basic_textarea.html" %}'
                '{% endwith %}'
            )
        elif type == 'number':
            elem = (
                '{% with id="' + str(id) + '", label="' + str(label) +
                '", value="' + value + '", l_attr=' + str(l_attr) +
                ', value=args[\'' + str(id) + '\'] %}'
                '{% include "elem/basic_number.html" %}'
                '{% endwith %}'
            )
        elif type == 'date':
            elem = (
                '{% with id="' + str(id) + '", label="' + str(label) +
                '", value="' + value + '", l_attr=' + str(l_attr) +
                ', value=args[\'' + str(id) + '\'] %}'
                '{% include "elem/basic_date.html" %}'
                '{% endwith %}'
            )
        elif type == 'datetime-local':
            elem = (
                '{% with id="' + str(id) + '", label="' + str(label) +
                '", value="' + value + '", l_attr=' + str(l_attr) +
                ', value=args[\'' + str(id) + '\'] %}'
                '{% include "elem/basic_datetime.html" %}'
                '{% endwith %}'
            )

        return elem

    @staticmethod
    def open_div(l_class=''):
        """
        Open a <div> with an optional CSS class.
        """
        if l_class == '':
            elem = '<div>'
        else:
            elem = ('<div class="' + l_class + '">')

        return elem

    @staticmethod
    def build_div_obj(id, obj_html, l_class=''):
        """
        Wrap an object HTML in a bootstrap-compatible div (one field container).
        """
        elem = ('<div id="div_' + id + '" class="form-group d-md-flex mt-1 my-md-2 ' + l_class + '">' + obj_html + '</div>')

        return elem

    @staticmethod
    def read_layout(data, l_obj_html):
        """
        Recursively read the 'layout.rows' section of TOML.
        This builds nested divs, rows, columns and injects elements by id.
        """
        for item in data:
            l_class = ''

            # Form.log.info(Logs.fileline() + ' : DEBUG read_layout data = ' + str(item))

            if isinstance(item, (dict, list)) and 'class' in item:
                l_class = item['class']

            Form.html_content += Form.open_div(l_class)

            if 'cols' in item:
                # Nested columns
                Form.read_layout(item['cols'], l_obj_html)
                Form.html_content += '</div><!-- close cols -->'
            elif isinstance(item, (dict, list)) and 'elements' in item:
                # Group of elements
                Form.read_layout(item['elements'], l_obj_html)
                Form.html_content += '</div><!-- close elements -->'
            elif isinstance(item, (dict, list)) and 'element' in item:
                # Single element reference
                name_obj_html = item['element']

                Form.html_content += Form.build_div_obj(name_obj_html, l_obj_html[name_obj_html], l_class)
                Form.html_content += '</div><!-- close element -->'

    @staticmethod
    def build_js_data(id, type, required):
        """
        Build the JS needed to:
        - read the field value when saving,
        - optionally normalize it (phone),
        - and enforce required fields.
        """
        if type in ('text', 'number', 'date', 'datetime-local', 'select'):
            Form.html_var += 'var ' + str(id) + ' = $("#' + str(id) + '").val() ;\n'

            if id in ('pat_phone1', 'pat_phone2'):
                # Remove spaces in phone numbers before sending
                Form.html_var += str(id) + ' = ' + str(id) + '.replaceAll(" ", "") ;\n'
        elif type in ('radio'):
            Form.html_var += 'var ' + str(id) + ' = $("input:radio[name=' + str(id) + ']:checked").val() ;\n'
        elif type in ('textarea'):
            Form.html_var += 'var ' + str(id) + ' = $.trim( $("#' + str(id) + '").val() ) ;\n'
        elif type in ('text_special'):
            # Read text content instead of value (used for pat_code label)
            Form.html_var += 'var ' + str(id) + ' = $("#' + str(id) + '").text() ;\n'

        # Keep a reference to this field in JSON param builder
        Form.json_var[str(id)] = str(id)

        # Required field validation (only if the element is visible)
        if required:
            Form.html_var += (
                'if (' + str(id) + ' === "" && !($("#' + str(id) + '").closest(":hidden").length > 0))\n'
                '{\n'
                '$("#' + str(id) + '").addClass("is-invalid");\n'
                'alert("{{ _("Veuillez saisir les champs obligatoires (*)") }}");\n'
                'return;\n'
                '}\n'
            )

    @staticmethod
    def build_history(form_toml, l_obj_html):
        """
        Build:
        - HTML containers for history tables (one per block),
        - JS for saving history items,
        - JS config for columns and labels,
        - JS for loading/deleting/filling history items.
        """
        history_js = ''

        try:
            from flask_babel import gettext as _

            form_elements = form_toml.get('description', {}).get('form_element', [])

            def get_label_for_field(field_id):
                """
                Find the label for a given field id in the TOML description.
                If not found, fallback to the id.
                """
                for e in form_elements:
                    if e.get('id') == field_id:
                        return e.get('label', field_id)
                return field_id

            history_cfg = form_toml.get('history', {})
            blocks = history_cfg.get('block', [])

            if isinstance(blocks, dict):
                blocks = [blocks]

            fields_by_block = {}

            # --- build HTML containers per block (tables + Enregistrer button) ---
            for block in blocks:
                block_id = block.get('id')
                if not block_id:
                    continue

                # List all fields belonging to this block (id starts with "block_id_")
                fields = []
                for e in form_elements:
                    elem_id = e.get('id')
                    if not elem_id or not isinstance(elem_id, str):
                        continue
                    if not elem_id.startswith(block_id + '_'):
                        continue
                    if 'input_type' not in e:
                        continue
                    fields.append(e)

                fields_by_block[block_id] = fields

                header_cells = ''
                header_cells += '<th>' + _("Action") + '</th>'
                header_cells += '<th>' + _("Date de saisie") + '</th>'
                header_cells += '<th>' + _("Utilisateur") + '</th>'

                # Columns declared in history.block.columns use field ids
                for col_id in block.get('columns', []):
                    label = get_label_for_field(col_id)
                    header_cells += '<th>' + _(label) + '</th>'

                table_html = (
                    '<table class="table table-sm table-striped history-table w-100">'
                    '<thead><tr>' + header_cells + '</tr></thead>'
                    '<tbody></tbody>'
                    '</table>'
                )

                block_html = (
                    '<div class="history-table-container w-100" style="min-height: 150px;" '
                    'data-history-block="' + str(block_id) + '">'
                    '<div class="table-responsive w-100">' +
                    table_html +
                    '</div>'
                    '<div class="d-flex justify-content-end mt-2">'
                    '<input type="button" '
                    'class="btn btn-lbk btn-{{ session[\'user_role\']|safe }}" '
                    'value="' + _("Enregistrer") + '" '
                    'onclick="save_hist_block_' + str(block_id) + '(id_pat);" />'
                    '</div>'
                    '</div>'
                )

                l_obj_html[block_id] = block_html

            js_parts = []

            # --- build JS save_hist_block_xxx() functions (one per block) ---
            for block in blocks:
                block_id = block.get('id')
                if not block_id:
                    continue

                fields = fields_by_block.get(block_id, [])
                if not fields:
                    continue

                lines = []
                lines.append('function save_hist_block_' + str(block_id) + '(id_pat) {')
                lines.append('    var param = {};')
                lines.append('    param.id_user = id_user;')
                lines.append('    param.block_id = "' + str(block_id) + '";')
                lines.append('    param.fields = {};')

                # Collect values from all fields belonging to this block
                for e in fields:
                    field_id = e.get('id')
                    input_type = e.get('input_type')
                    if not field_id or not input_type:
                        continue

                    required = False
                    for key, val in e.items():
                        if key.startswith('attr_'):
                            attr_name = key.replace('attr_', '')
                            if attr_name == 'required' and val:
                                required = True

                    if input_type in ('text', 'number', 'date', 'datetime-local', 'select'):
                        lines.append('    var ' + field_id + ' = $("#' + field_id + '").val();')
                    elif input_type == 'radio':
                        lines.append('    var ' + field_id + ' = $("input:radio[name=' + field_id + ']:checked").val();')
                    elif input_type == 'textarea':
                        lines.append('    var ' + field_id + ' = $.trim($("#' + field_id + '").val());')
                    else:
                        lines.append('    var ' + field_id + ' = $("#' + field_id + '").val();')

                    if required:
                        lines.append('    if (' + field_id + ' === "" && !($("#' + field_id + '").closest(":hidden").length > 0)) {')
                        lines.append('        $("#' + field_id + '").addClass("is-invalid");')
                        lines.append('        alert("{{ _("Veuillez saisir les champs obligatoires (*)") }}");')
                        lines.append('        return;')
                        lines.append('    }')

                    lines.append("    param.fields['" + field_id + "'] = " + field_id + ';')

                # If an event is currently loaded and nothing changed, do not save
                lines.append('    if (patHistCurrent["' + str(block_id) + '"] && isSameHistFields("' + str(block_id) + '", param.fields)) {')
                lines.append('        alert("{{ _("Aucune modification détectée, rien à enregistrer.") }}");')
                lines.append('        return;')
                lines.append('    }')

                # Confirm only if there are real changes
                lines.append('    if (!confirm("{{ _("Voulez-vous enregistrer cet élément ?") }}")) { return; }')

                lines.append('    if (!id_pat || id_pat <= 0) {')
                lines.append('        alert("{{ _("Le patient doit être enregistré avant de saisir l’historique.") }}");')
                lines.append('        return;')
                lines.append('    }')

                # POST history item to backend
                lines.append('    $.ajax({')
                lines.append("        type: 'POST',")
                lines.append("        url: '{{ session['server_ext'] }}/services/patient/history/form/item/' + id_pat,")
                lines.append("        dataType: 'json',")
                lines.append("        contentType: 'application/json; charset=utf-8',")
                lines.append("        data: JSON.stringify(param),")
                lines.append("        headers: { 'Authorization': 'Bearer {{ session.get('be_access_token', '') }}' },")
                lines.append("        success: function(data) {")
                lines.append("            $('#toast-msg').text(\"{{ _('Enregistrement effectué') }}\");")
                lines.append("            $('.toast').toast('show');")

                # Reset fields and reload history
                for e in fields:
                    fid = e.get('id')
                    if not fid:
                        continue
                    lines.append("            $('#" + fid + "').val('');")
                    lines.append("            $('#" + fid + "').removeClass('is-invalid');")

                lines.append("            load_patient_hist(id_pat);")
                # Clear current event for this block
                lines.append('            patHistCurrent["' + str(block_id) + '"] = null;')
                lines.append("        },")
                lines.append("        error: function(xhr, status, error) {")
                lines.append("            alert(\"{{ _('Une erreur est survenue lors de l’enregistrement') }}\");")
                lines.append("        }")
                lines.append("    });")
                lines.append("}")

                js_parts.append('\n'.join(lines))

            # --- build column configuration and labels per block ---
            cfg_lines = []
            cfg_lines.append('var patHistConfig = {};')
            cfg_lines.append('var patHistLabels = {};')
            for block in blocks:
                block_id = block.get('id')
                if not block_id:
                    continue

                cols = block.get('columns', [])
                cols_js = '[' + ', '.join(['"' + c + '"' for c in cols]) + ']'
                cfg_lines.append('patHistConfig["' + str(block_id) + '"] = ' + cols_js + ';')

                # Build label map: field id -> translated label
                label_pairs = []
                fields = fields_by_block.get(block_id, [])
                for fe in fields:
                    fid = fe.get('id')
                    if not fid:
                        continue
                    col_label = fe.get('label', fid)
                    col_label = _(col_label)
                    col_label = col_label.replace('"', '\\"')
                    label_pairs.append('"' + fid + '": "' + col_label + '"')

                cfg_lines.append('patHistLabels["' + str(block_id) + '"] = {' + ', '.join(label_pairs) + '};')

            js_parts.append('\n'.join(cfg_lines))

            # --- shared JS: load, fill form, delete ---
            common_js = r'''
            var patHistData = [];
            var patHistCurrent = {}; // current loaded event per block

            function formatHistFieldValue(fieldId, rawVal) {
                if (!rawVal) { return ""; }
                var v = String(rawVal);

                if (fieldId.indexOf("_datetime") !== -1) {
                    v = v.replace("T", " ");
                    if (v.length >= 16) {
                        v = v.substring(0, 16);
                    }
                    return v;
                }
                return v;
            }

            function isSameHistFields(blockId, newFields) {
                var curObj = patHistCurrent[blockId];
                if (!curObj || !curObj.fields) { return false; }

                var cur = curObj.fields || {};
                var newKeys = Object.keys(newFields);
                var curKeys = Object.keys(cur);

                if (newKeys.length !== curKeys.length) {
                    return false;
                }

                for (var i = 0; i < newKeys.length; i++) {
                    var k = newKeys[i];
                    if (cur[k] !== newFields[k]) {
                        return false;
                    }
                }

                return true;
            }

            function hist_fill_form(evt_id, blockId) {
                if (!patHistData || !patHistData.length) { return; }
                var found = null;
                for (var i = 0; i < patHistData.length; i++) {
                    if (String(patHistData[i].evt) === String(evt_id)) {
                        found = patHistData[i];
                        break;
                    }
                }
                if (!found) { return; }

                var fields = found.fields || {};

                // Keep original values for change detection on save
                patHistCurrent[blockId] = {
                    evt: found.evt,
                    fields: $.extend({}, fields)
                };

                Object.keys(fields).forEach(function(k) {
                    var rawVal = fields[k];

                    // Handle radio group first
                    var $radioGroup = $('input:radio[name="' + k + '"]');
                    if ($radioGroup.length) {
                        $radioGroup.prop('checked', false);
                        $radioGroup.filter('[value="' + rawVal + '"]').prop('checked', true);
                        return;
                    }

                    var $field = $('#' + k);
                    if (!$field.length) {
                        return;
                    }

                    var tag = ($field.prop('tagName') || '').toLowerCase();
                    var type = ($field.attr('type') || '').toLowerCase();

                    if (tag === 'input') {
                        $field.val(rawVal);
                    } else if (tag === 'textarea' || tag === 'select') {
                        $field.val(rawVal);
                    }

                    $field.removeClass('is-invalid');
                });
            }

            function load_patient_hist(id_pat) {
                if (!id_pat || id_pat <= 0) { return; }

                $.ajax({
                    type: 'GET',
                    url: '{{ session["server_ext"] }}/services/patient/history/form/item/' + id_pat,
                    dataType: 'json',
                    headers: { 'Authorization': 'Bearer {{ session.get("be_access_token", "") }}' },
                    success: function(data) {
                        patHistData = data || [];

                        // Destroy existing DataTables instances on history tables
                        if ($.fn.DataTable) {
                            $('.history-table').each(function () {
                                if ($.fn.DataTable.isDataTable(this)) {
                                    $(this).DataTable().destroy();
                                }
                            });
                        }

                        // Clear all table bodies
                        $('.history-table-container').each(function() {
                            $(this).find('tbody').empty();
                        });

                        if (!data || !data.length) {
                            return;
                        }

                        data.forEach(function(evt) {
                            var blockId = evt.block_id;
                            if (!blockId || !patHistConfig[blockId]) { return; }

                            var selector = '.history-table-container[data-history-block="' + blockId + '"] tbody';
                            var $tbody = $(selector);
                            if (!$tbody.length) { return; }

                            var cols = patHistConfig[blockId];
                            var fields = evt.fields || {};

                            var $tr = $('<tr></tr>');

                            var $tdActions = $('<td></td>');
                            var $nav = $('<nav></nav>');
                            var $ul = $('<ul class="navbar-nav"></ul>');
                            var $li = $('<li class="nav-item dropdown"></li>');
                            var $toggle = $('<a class="dropdown-toggle menu-act" data-bs-toggle="dropdown"></a>');
                            var $menu = $('<div class="dropdown-menu menu-act-drop nav-style" style="padding:0;"></div>');

                            var $aDetails = $('<a class="dropdown-item menu-act-item" href="#"></a>');
                            {% if has_permission("RECORD_25") %}
                            var $aDelete = $('<a class="dropdown-item menu-act-item" href="#"></a>');
                            $aDelete.text("{{ _("Supprimer") }}");
                            $aDelete.on('click', function(e) {
                                e.preventDefault();
                                hist_delete_item(evt.evt);
                            });
                            $menu.append($aDelete);
                            {% endif %}

                            $li.append($toggle);
                            $li.append($menu);
                            $ul.append($li);
                            $nav.append($ul);
                            $tdActions.append($nav);
                            $tr.append($tdActions);

                            var $tdDate = $('<td></td>');
                            $tdDate.text(evt.datetime || '');
                            $tr.append($tdDate);

                            var $tdUser = $('<td></td>');
                            var userLabel = evt.user_name || evt.id_user || '';
                            $tdUser.text(userLabel);
                            $tr.append($tdUser);

                            cols.forEach(function(colId) {
                                var $td = $('<td></td>');
                                var val = fields[colId];
                                if (val === undefined || val === null) { val = ''; }
                                val = formatHistFieldValue(colId, val);
                                $td.text(val);
                                $tr.append($td);
                            });

                            // Click on row -> fill form with all fields from the event
                            $tr.on('click', function(e) {
                                // Do not interfere when clicking inside the dropdown menu
                                if ($(e.target).closest('.dropdown-menu').length) {
                                    return;
                                }
                                hist_fill_form(evt.evt, blockId);
                            });

                            $tbody.append($tr);
                        });

                        // Initialize DataTables on history tables (sorting + paging, no search)
                        if ($.fn.DataTable) {
                            $('.history-table').DataTable({
                                searching: false,      // no search box
                                paging: true,
                                ordering: true,
                                lengthChange: false,   // no "show X entries"
                                pageLength: 10,
                                language: {
                                    lengthMenu: "{{ _('Afficher _MENU_ entrées') }}",
                                    zeroRecords: "{{ _('Aucun enregistrement trouvé') }}",
                                    info: "{{ _('Affichage de _START_ à _END_ sur _TOTAL_ entrées') }}",
                                    infoEmpty: "{{ _('Aucune entrée disponible') }}",
                                    infoFiltered: "{{ _('(filtré de _MAX_ entrées au total)') }}",
                                    paginate: {
                                        first: "{{ _('Premier') }}",
                                        last: "{{ _('Dernier') }}",
                                        next: "{{ _('Suivant') }}",
                                        previous: "{{ _('Précédent') }}"
                                    }
                                }
                            });
                        }
                    },
                    error: function(xhr, status, error) {
                        alert("{{ _('Une erreur est survenue lors du chargement') }}");
                    }
                });
            }

            function hist_delete_item(evt_id) {
                if (!id_pat || id_pat <= 0) {
                    alert("{{ _("Patient invalide") }}");
                    return;
                }
                if (!confirm("{{ _("Voulez-vous supprimer cet élément ?") }}")) {
                    return;
                }
                $.ajax({
                    type: 'DELETE',
                    url: '{{ session["server_ext"] }}/services/patient/history/form/item/' + id_pat + '/' + evt_id,
                    dataType: 'json',
                    headers: { 'Authorization': 'Bearer {{ session.get("be_access_token", "") }}' },
                    success: function(data) {
                        $('#toast-msg').text("{{ _("Suppression effectuée") }}");
                        $('.toast').toast('show');
                        load_patient_hist(id_pat);
                    },
                    error: function(xhr, status, error) {
                        alert("{{ _("Une erreur est survenue lors de la suppression") }}");
                    }
                });
            }

            $(document).ready(function() {
                load_patient_hist(id_pat);
            });
            '''
            js_parts.append(common_js.strip())

            if js_parts:
                # Concatenate all JS parts (block-specific + shared)
                history_js = '\n\n'.join(js_parts)

        except Exception as err:
            # If history building fails, log and at least create empty containers
            Form.log.error(Logs.fileline() + ' : failed to build history tables/JS, err=%s', err)

            history_cfg = form_toml.get('history', {})
            blocks = history_cfg.get('block', [])
            if isinstance(blocks, dict):
                blocks = [blocks]

            for block in blocks:
                block_id = block.get('id')
                if block_id and block_id not in l_obj_html:
                    l_obj_html[block_id] = (
                        '<div class="history-table-container" '
                        'data-history-block="' + str(block_id) + '"></div>'
                    )

        return history_js
