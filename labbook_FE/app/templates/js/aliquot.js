{#
    Aliquot handling shared by the single-record and multi-record result pages.
    Requires the globals cur_id_samp, cur_samp_type and cur_id_pat, and the
    popup/popup_aliquot.html modal.
    Set aliquot_audit before including to wrap the save call in an audit context.
#}
function add_aliquot(id_samp, samp_type, id_pat)
{
cur_id_samp = id_samp;
cur_samp_type = samp_type;
cur_id_pat = id_pat;

let firstForm = document.querySelector(".aliquot_form");

    if (firstForm) 
    {
        firstForm.querySelector(".pathogen").value = "";
        firstForm.querySelector(".coordinates").value = "";
        firstForm.querySelector(".in_stock").checked = true;
        firstForm.querySelector(".box").selectedIndex = 0;
        firstForm.querySelector(".box_coord").textContent = "";
    }

document.querySelectorAll(".aliquot_form:not(:first-child), .aliquot-separator").forEach(elem => elem.remove());

let aliquotModal = new bootstrap.Modal(document.getElementById('aliquotModal'));
aliquotModal.show();
}

function saveAliquot() 
{
let aliquots = [];

    document.querySelectorAll(".aliquot_form").forEach(form => 
    {
        let pathogen = form.querySelector(".pathogen").value;  
        let coord = form.querySelector(".coordinates").value;  
        let in_stock = form.querySelector(".in_stock").checked ? "Y" : "N";  
        let box = form.querySelector(".box").value;

        if (!box || box == "0") {
            alert("{{ _("L'association à une boîte est obligatoire.") }}");
            return false;
        }

        let aliquotData = {
            sal_user: {{ session['user_id']|safe }},
            sal_type: cur_samp_type,
            sal_sample: cur_id_samp,
            sal_patient: cur_id_pat,
            sal_pathogen: pathogen,
            sal_coordinates: coord,
            sal_in_stock: in_stock,
            sal_box: box
        };

        aliquots.push(aliquotData) ;
    } ) ;

{% if aliquot_audit %}
    set_audit_context("{{ _('Enregistrement aliquot') }}");
{% endif %}
    fetch("{{ session['server_ext'] }}/services/quality/storage/aliquot/det/0", {
        method: "POST",
        headers: {% if aliquot_audit %}with_audit_headers({ "Authorization": "Bearer {{ session.get('be_access_token','') }}", "Content-Type": "application/json" }){% else %}{ "Authorization": "Bearer {{ session.get('be_access_token','') }}", "Content-Type": "application/json" }{% endif %},
        body: JSON.stringify({ aliquots: aliquots })
    })
    .then(response => {
        if (response.status === 200 || response.status === 204) {
            return;
        }
        return response.json().catch(() => ({}));
    })
    .then(data => {
        if (data && data.error) 
        {
            alert("{{ _("Une erreur est survenue lors de l'enregistrement") }}");
        }
        else
        {
        let modal = bootstrap.Modal.getInstance(document.getElementById('aliquotModal'));
            modal.hide();

            setTimeout(() => {
                let toast = new bootstrap.Toast(document.getElementById('toastSuccess'));
                toast.show();
            }, 500);
        }
    })
    .catch(error => alert("{{ _("Une erreur est survenue lors de l'enregistrement") }}") );
}

document.getElementById("more_aliquot").addEventListener("click", function() 
{
    let newAliquot = document.querySelector(".aliquot_form").cloneNode(true);

    let separator = document.createElement("hr");
    separator.classList.add("aliquot-separator");

    let removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.className = "btn btn-danger btn-sm remove-aliquot";
    removeButton.innerHTML = "<i class='bi bi-trash'></i> {{ _('Supprimer') }}";
    removeButton.style.marginTop = "10px";

    removeButton.addEventListener("click", function() {
        separator.remove();
        newAliquot.remove();
    });

    let newBoxCoord = newAliquot.querySelector(".box_coord");
    if (newBoxCoord) {
        newBoxCoord.textContent = "";
    }

    newAliquot.appendChild(removeButton);

    let aliquotList = document.getElementById("aliquotList");
    aliquotList.appendChild(separator);
    aliquotList.appendChild(newAliquot);
});

function get_box_coord(event) 
{
let boxSelect = event.target;
let boxId = boxSelect.value;

let aliquotForm = boxSelect.closest(".aliquot_form");
let boxCoordSpan = aliquotForm.querySelector(".box_coord");

    if (boxId) {
        let url = `{{ session['server_ext'] }}/services/quality/storage/box/coord/${boxId}`;

        fetch(url, {
            headers: { "Authorization": "Bearer {{ session.get('be_access_token','') }}" }
            })
            .then(response => response.json())
            .then(data => {
                if (data.sbo_label) {
                    let coordText = `${data.sro_label || ''} > ${data.sch_label || ''} > ${data.sco_label || ''} > ${data.sbo_label}`;
                    
                    if (data.sbo_coordinates) {
                        coordText += ` [${data.sbo_coordinates}]`;
                    } 

                    if (data.sbo_full === "Y") {
                        coordText += " ({{ _('Pleine') }})";
                    }

                    boxCoordSpan.textContent = coordText;
                }
            })
            .catch(() => {
                boxCoordSpan.textContent = "{{ _("Erreur lors de la récupération") }}";
            });
    } else {
        boxCoordSpan.textContent = "";
    }
}
