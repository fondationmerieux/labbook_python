/* =========================================================
   SEND REPORT - shared logic
   ========================================================= */

/* ---------- helpers ---------- */

function hasEmail(){ return (patEmail && patEmail.trim() !== ''); }
function hasPhone(){ return ((patPhone1 && patPhone1.trim()!=='') || (patPhone2 && patPhone2.trim()!=='')); }
function getPhone(){ return (patPhone1 && patPhone1.trim()!=='') ? patPhone1.trim() : (patPhone2||'').trim(); }
function hasDocEmail(){ return (docEmail && docEmail.trim() !== ''); }
function hasDocPhone(){ return (docPhone && docPhone.trim() !== ''); }

/* ---------- normalization ---------- */

function normMethod(m) {
    return {
        id: String(m.sdi_ser),
        code: String(m.sdi_type || '').toUpperCase(),
        label: m.sdi_name,
        isDefault: m.sdi_default === 'Y'
    };
}

function normModel(t) {
    return {
        id: String(t.mdl_ser),
        code: String(t.mdl_type || '').toUpperCase(),
        name: t.mdl_displayname
    };
}

/* ---------- core ---------- */

function modelsForMethod(method) {
    const code = String(method?.code || '').toUpperCase();

    // AmiCare
    if (code === 'A') return [];

    return (SEND_MODELS || []).map(normModel).filter(x => x.code === code);
}

function methodPossible(m) {
    if (m.code === 'A') return true;
    return modelsForMethod(m).length > 0;
}

function orderMethods(methodsAll) {
    const possible = methodsAll.filter(methodPossible);
    const def = methodsAll.find(x => x.isDefault) || null;

    if (def && possible.some(x => String(x.id) === String(def.id))) {
        return [def, ...possible.filter(x => String(x.id) !== String(def.id))];
    }

    return possible;
}

/* ---------- init ---------- */

function initSendInline() {
    if (!Array.isArray(SEND_METHODS)) return;

    let methods = SEND_METHODS.map(normMethod);

    // --- AmiCare injection ---
    const amicareEnabled = AMICARE_CFG && AMICARE_CFG.enabled;
    const hasAmicarePatient = PAT_AMICARE > 0;

    if (amicareEnabled && hasAmicarePatient) {
        methods.unshift({
            id: "0",
            code: "A",
            label: "AmiCare",
            isDefault: true
        });
    }

    methods = orderMethods(methods);

    const select = document.querySelector("#send_method_last");
    if (!select) return;

    select.innerHTML = "";

    methods.forEach(m => {
        const opt = document.createElement("option");
        opt.value = m.id;
        opt.textContent = m.label;
        opt.dataset.code = m.code;
        select.appendChild(opt);
    });

    // AmiCare
    if (amicareEnabled && hasAmicarePatient) {
        select.selectedIndex = 0;
    }

    select.addEventListener("change", onMethodChange);

    onMethodChange();
}

function onMethodChange() {
    const select = document.querySelector("#send_method_last");
    if (!select) return;

    const selected = select.options[select.selectedIndex];
    if (!selected) return;
    const code = selected.dataset.code;

    const modelSelect = document.querySelector("#send_model_last");
    if (!modelSelect) return;

    modelSelect.innerHTML = "";

    const recip = document.querySelector("#send_recipient_last");

    if (code === 'A') {
        modelSelect.style.display = "none";
        setHelp("");

        if (recip) {
            recip.value = "";
            recip.disabled = true;
        }

        updateToggleTooltip();

        return;
    }

    // Prefill recipient based on consent
    if (recip) {
        recip.value = "";
        recip.type = (code === 'W') ? 'tel' : 'email';

        if (patAgreement === 'Y') {
            if (code === 'W') {
                recip.value = getPhone();
            } else {
                recip.value = patEmail || "";
            }
            currentRecipientSource = "PAT";
        }
        else if (docAgreement === 'Y') {
            if (code === 'W') {
                recip.value = docPhone || "";
            } else {
                recip.value = docEmail || "";
            }
            currentRecipientSource = "DOC";
        } else {
            recip.value = "";
            currentRecipientSource = null;
        }
    }

    if (code === 'W') {
        setHelp("{{ _('WhatsApp attend un numéro au format international (+33...)') }}");
    } else if (code === 'S' || code === 'M') {
        setHelp("{{ _('Méthode email : renseigner une adresse valide.') }}");
    } else {
        setHelp("");
    }

    if (recip) {
        recip.disabled = false;
    }

    const models = modelsForMethod({ code });

    modelSelect.style.display = "inline-block";

    if (!models.length) {
        const opt = document.createElement("option");
        opt.value = "";
        opt.textContent = "{{ _('Aucun modèle') }}";
        modelSelect.appendChild(opt);
    } else {
        models.forEach(m => {
            const opt = document.createElement("option");
            opt.value = m.id;
            opt.textContent = m.name;
            modelSelect.appendChild(opt);
        });
    }

    updateToggleTooltip();

    if (models.length) {
        if (code !== 'W' && code !== 'S' && code !== 'M') {
            setHelp("");
        }
    }
}

function send_last_report(file) {
    const methodSel = document.querySelector("#send_method_last");
    const modelSel  = document.querySelector("#send_model_last");
    const recip     = document.querySelector("#send_recipient_last");

    if (!methodSel) return;

    const method = methodSel.options[methodSel.selectedIndex];
    if (!method) return;

    const code = method.dataset.code;
    const methodId = method.value;
    const recipient = recip ? recip.value.trim() : "";

    const modelId = (code === 'A') ? 0 : (modelSel ? modelSel.value : null);

    // ---------------- VALIDATION ----------------

    if (!methodId) {
        setHelp("{{ _('Sélectionnez une méthode.') }}");
        return;
    }

    if (code !== 'A' && !modelId) {
        setHelp("{{ _('Aucun modèle') }}");
        return;
    }

    if (code !== 'A' && !recipient) {
        setHelp("{{ _('Destinataire') }}");
        return;
    }

    if (code === 'W') {
        const phone = recipient.replace(/\s+/g, '');
        if (!/^\+\d{6,}$/.test(phone)) {
            setHelp("{{ _('WhatsApp attend un numéro au format international (+33...)') }}");
            return;
        }
    }

    if (code === 'S' || code === 'M') {
        const ok = recip.checkValidity();
        if (!ok) {
            setHelp("{{ _('Méthode email : renseigner une adresse valide.') }}");
            return;
        }
    }

    // ---------------- UI ----------------

    setHelp("");
    $("#dial-wait").modal("show");

    // ---------------- CALL ----------------

    $.ajax({
        type: "POST",
        url: "{{ session['server_ext'] }}/services/setting/sending/report",
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            method_id: methodId,
            method_type: code,
            template_id: modelId,
            recipient: recipient,
            file: file,
            rec_num: num_rec,
            pat_code: pat_code,
            pat_amicare: PAT_AMICARE,
            id_user: id_user
        }),
        headers: { 'Authorization': 'Bearer {{ session.get("be_access_token","") }}' },

        success: function() {
            $("#dial-wait").modal("hide");
            setHelp("{{ _('Rapport envoyé') }}");
        },

        error: function(xhr) {
            $("#dial-wait").modal("hide");

            const msg =
                xhr?.responseJSON?.error ||
                xhr?.responseText ||
                "Erreur envoi";

            setHelp(msg);
        }
    });
}

let currentRecipientSource = "PAT";

function toggleRecipient() {
    const input = document.querySelector("#send_recipient_last");
    if (!input) return;

    if (currentRecipientSource === "PAT") {
        if (docEmail && docEmail.trim() !== "") {
            input.value = docEmail;
        } else if (docPhone && docPhone.trim() !== "") {
            input.value = docPhone;
        }
        currentRecipientSource = "DOC";
    } else {
        if (patEmail && patEmail.trim() !== "") {
            input.value = patEmail;
        } else if (patPhone1 && patPhone1.trim() !== "") {
            input.value = patPhone1;
        } else if (patPhone2 && patPhone2.trim() !== "") {
            input.value = patPhone2;
        }
        currentRecipientSource = "PAT";
    }

    updateToggleTooltip();
}

function setHelp(msg) {
    const el = document.querySelector("#send_inline_help_last");
    if (el) el.textContent = msg || "";
}

function updateToggleTooltip() {
    const btn = document.querySelector("#btn_toggle_recipient");
    if (!btn) return;

    let txt = "";

    if (currentRecipientSource === "PAT") {
        txt = "{{ _('Récupérer les informations du praticien') }}";
    } else if (currentRecipientSource === "DOC") {
        txt = "{{ _('Récupérer les informations du patient') }}";
    } else {
        txt = "";
    }

    btn.setAttribute("title", txt);
}
