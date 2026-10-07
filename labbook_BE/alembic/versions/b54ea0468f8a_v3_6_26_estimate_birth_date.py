# -*- coding:utf-8 -*-
"""v3_6_26_estimate_birth_date

Revision ID: b54ea0468f8a
Revises: 1d7606550c77
Create Date: 2026-10-01 18:33:18.127926

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'b54ea0468f8a'
down_revision = '1d7606550c77'
branch_labels = None
depends_on = None


OWNER_ID = 1


def create_analysis(conn, owner_id, analysis_def, vars_def, links_def):
    var_ids = {}

    for v in vars_def:
        if isinstance(v["type_resultat"], str):
            row_type = conn.execute(text("""
                SELECT id_data FROM sigl_dico_data
                WHERE dico_name = 'type_resultat' AND label = :label LIMIT 1"""), {"label": v["type_resultat"]}).fetchone()

            if not row_type:
                print("ERROR type_resultat not found,\n\ttype_resultat=" + str(v["type_resultat"]))
                continue

            type_resultat = row_type.id_data
        else:
            type_resultat = v["type_resultat"]

        res = conn.execute(text("""
            INSERT INTO sigl_07_data (
                id_owner, libelle, description, unite, normal_min, normal_max, commentaire,
                type_resultat, unite2, formule_unite2, formule, accuracy, precision2,
                code_var, var_highlight, var_show_minmax, var_in_report
            )
            VALUES (
                :id_owner, :libelle, '', :unite, :normal_min, :normal_max, '',
                :type_resultat, 0, '', '', :accuracy, 0, :code_var, 'N', 'N', 'Y'
            )
            ON DUPLICATE KEY UPDATE id_data = LAST_INSERT_ID(id_data)"""), {
            "id_owner": owner_id, "libelle": v["libelle"], "unite": v["unite"], "normal_min": v["normal_min"],
            "normal_max": v["normal_max"], "type_resultat": type_resultat, "accuracy": v["accuracy"],
            "code_var": v["code_var"]})

        var_ids[v["code_var"]] = res.lastrowid

    row = conn.execute(text("""
        SELECT id_data FROM sigl_05_data
        WHERE id_owner = :id_owner AND code = :code
        LIMIT 1"""), {"id_owner": owner_id, "code": analysis_def["code"]}).fetchone()

    if row:
        ana_id = row.id_data

    else:
        res = conn.execute(text("""
            INSERT INTO sigl_05_data (
                id_owner, code, nom, abbr, famille, cote_unite, cote_valeur,
                commentaire, produit_biologique, type_prel, type_analyse,
                actif, ana_whonet, ana_ast, ana_loinc, ana_lite
            )
            VALUES (
                :id_owner, :code, :nom, :abbr, :famille, :cote_unite, :cote_valeur,
                :commentaire, :produit_biologique, :type_prel, :type_analyse,
                4, 5, 'N', :ana_loinc, 'N'
            )
        """), {
            "id_owner": owner_id,
            "code": analysis_def["code"],
            "nom": analysis_def["nom"],
            "abbr": analysis_def["abbr"],
            "famille": analysis_def["famille"],
            "cote_unite": analysis_def["cote_unite"],
            "cote_valeur": analysis_def["cote_valeur"],
            "commentaire": analysis_def["commentaire"],
            "produit_biologique": analysis_def["produit_biologique"],
            "type_prel": analysis_def["type_prel"],
            "type_analyse": analysis_def["type_analyse"],
            "ana_loinc": analysis_def["ana_loinc"],
        })

        ana_id = res.lastrowid

    for code_var, position, num_var in links_def:
        id_refvariable = var_ids.get(code_var)

        if not id_refvariable:
            continue

        existing = conn.execute(text("""
            SELECT id_data FROM sigl_05_07_data
            WHERE id_owner = :id_owner AND id_refanalyse = :id_refanalyse AND id_refvariable = :id_refvariable
            LIMIT 1"""), {"id_owner": owner_id, "id_refanalyse": ana_id, "id_refvariable": id_refvariable}).fetchone()

        if existing:
            continue

        conn.execute(text("""
            INSERT INTO sigl_05_07_data (
                id_owner, id_refanalyse, id_refvariable, position, num_var, obligatoire, var_whonet, var_qrcode
            )
            VALUES (
                :id_owner, :id_refanalyse, :id_refvariable, :position, :num_var, 4, 5, 'N'
            )"""), {"id_owner": owner_id, "id_refanalyse": ana_id, "id_refvariable": id_refvariable,
                    "position": position, "num_var": num_var})


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_6_26_estimate_birth_date revision=b54ea0468f8a")

    # Get the current
    conn = op.get_bind()

    # ESTIMATE birth date of patients with only an age, from the receipt date of their last record
    try:
        ret = conn.execute(text("update sigl_03_data as pat "
                                "inner join (select id_patient, date(max(rec_date_receipt)) as ref_date "
                                "from sigl_02_data where rec_date_receipt is not NULL group by id_patient) as rec "
                                "on rec.id_patient = pat.id_data "
                                "set pat.ddn = case pat.unite "
                                "when 1037 then rec.ref_date - interval pat.age year "
                                "when 1036 then rec.ref_date - interval pat.age month "
                                "when 1035 then rec.ref_date - interval pat.age week "
                                "when 1034 then rec.ref_date - interval pat.age day end, "
                                "pat.ddn_approx = 4 "
                                "where pat.ddn is NULL and pat.age > 0 and pat.unite in (1034, 1035, 1036, 1037)"))
        print("estimated birth date for " + str(ret.rowcount) + " patients")
    except Exception as err:
        print("ERROR estimate birth date for sigl_03_data,\n\terr=" + str(err))

    # --- Roche cobas 5800 viral loads, each with a numeric and a qualitative variable ---
    try:
        analysis_def = {
            "code": "HIV_VL", "nom": "Charge virale VIH-1", "abbr": "HIV-1",
            "famille": 17, "cote_unite": "B", "cote_valeur": 0,
            "commentaire": "Automate Roche cobas 5800",
            "produit_biologique": 0, "type_prel": 138,
            "type_analyse": 170, "ana_loinc": "70241-5"
        }

        vars_def = [
            {"code_var": "HIV_VL", "libelle": "Charge virale VIH-1", "unite": 1181, "normal_min": "", "normal_max": "", "type_resultat": 226, "accuracy": 0},
            {"code_var": "HIV_QUAL", "libelle": "VIH-1 qualitatif", "unite": 0, "normal_min": "", "normal_max": "", "type_resultat": 226, "accuracy": 0},
        ]

        links_def = [("HIV_VL", 10, 1), ("HIV_QUAL", 20, 2)]

        create_analysis(conn, OWNER_ID, analysis_def, vars_def, links_def)

    except Exception as err:
        print("ERROR create analysis HIV_VL,\n\terr=" + str(err))

    try:
        analysis_def = {
            "code": "HBV_VL", "nom": "Charge virale VHB", "abbr": "HBV",
            "famille": 17, "cote_unite": "B", "cote_valeur": 0,
            "commentaire": "Automate Roche cobas 5800",
            "produit_biologique": 0, "type_prel": 138,
            "type_analyse": 170, "ana_loinc": "42595-9"
        }

        vars_def = [
            {"code_var": "HBV_VL", "libelle": "Charge virale VHB", "unite": 293, "normal_min": "", "normal_max": "", "type_resultat": 226, "accuracy": 0},
            {"code_var": "HBV_QUAL", "libelle": "VHB qualitatif", "unite": 0, "normal_min": "", "normal_max": "", "type_resultat": 226, "accuracy": 0},
        ]

        links_def = [("HBV_VL", 10, 1), ("HBV_QUAL", 20, 2)]

        create_analysis(conn, OWNER_ID, analysis_def, vars_def, links_def)

    except Exception as err:
        print("ERROR create analysis HBV_VL,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration v3_6_26_estimate_birth_date revision=b54ea0468f8a")


def downgrade():
    """
    No-op by design.

    This migration is intentionally irreversible per the organization's
    forward-only policy. To roll back, restore a verified backup
    taken before revision b54ea0468f8a.
    """
    print("downgrade skipped: irreversible migration b54ea0468f8a (forward-only policy)")
