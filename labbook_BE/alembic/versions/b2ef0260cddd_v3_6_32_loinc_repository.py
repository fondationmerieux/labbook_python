# -*- coding:utf-8 -*-
"""v3_6_32_loinc_repository

Revision ID: b2ef0260cddd
Revises: 8875bc01ee99
Create Date: 2026-11-16 09:00:00.000000

"""
import json

from alembic import op
from sqlalchemy import text

from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'b2ef0260cddd'
down_revision = '8875bc01ee99'
branch_labels = None
depends_on = None

# LOINC analyses of the JDV ANS "Circuit de la biologie", work of the Fondation Merieux on a 3.6.30 base
LOINC_DATA = 'alembic/data/loinc_jdv_1_1_24.json'


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration v3_6_32_loinc_repository revision=b2ef0260cddd")

    conn = op.get_bind()

    # Long UCUM units in the code of dictionaries
    try:
        conn.execute(text("alter table sigl_dico_data modify code varchar(32) DEFAULT NULL"))
    except Exception as err:
        print("ERROR modify column sigl_dico_data.code,\n\terr=" + str(err))

    try:
        with open(LOINC_DATA, encoding='utf-8') as f:
            data = json.load(f)
    except Exception as err:
        print("ERROR read " + LOINC_DATA + ",\n\terr=" + str(err))
        return

    # Savepoint : the LOINC repository is added completely or not at all
    try:
        with conn.begin_nested():
            add_loinc_repository(conn, data)
    except Exception as err:
        print("ERROR add LOINC repository,\n\terr=" + str(err))

    try:
        with conn.begin_nested():
            fix_old_repository(conn, data['old_repository'])
    except Exception as err:
        print("ERROR fix old repository,\n\terr=" + str(err))

    # Description of dictionaries, existing ones are kept
    try:
        for dico_name, descr in data['dico_descr'].items():
            conn.execute(text("update sigl_dico_data set dico_descr=:descr "
                              "where dico_name=:name and (dico_descr is null or dico_descr='')"),
                         {"descr": descr, "name": dico_name})
    except Exception as err:
        print("ERROR description of dictionaries,\n\terr=" + str(err))

    sort_dictionaries(conn)

    print(str(datetime.today()) + " : END of migration v3_6_32_loinc_repository revision=b2ef0260cddd")


def add_loinc_repository(conn, data):
    if conn.execute(text("select id_data from sigl_05_data where code='L0001'")).fetchone():
        print("LOINC repository already present, nothing added")
        return

    # Dictionary entries : existing ones found again, missing ones created
    dico_ids = {}

    for d in data['dico']:
        id_dico = None

        if 'old' in d:
            old = d['old']
            row = conn.execute(text("select id_data, label, short_label, code from sigl_dico_data "
                                    "where id_data=:id and dico_name=:name"),
                               {"id": old['id'], "name": d['dico_name']}).fetchone()

            if row:
                id_dico = row.id_data

                # LOINC or SPM-4 code given to an existing entry, only if the laboratory did not change it
                for col in ('label', 'short_label', 'code'):
                    if d[col] != old[col] and getattr(row, col) == old[col]:
                        conn.execute(text("update sigl_dico_data set " + col + "=:val where id_data=:id"),
                                     {"val": d[col], "id": id_dico})
            else:
                row = conn.execute(text("select id_data from sigl_dico_data "
                                        "where dico_name=:name and binary label=:label order by id_data limit 1"),
                                   {"name": d['dico_name'], "label": d['label']}).fetchone()
                if row:
                    id_dico = row.id_data
        else:
            row = conn.execute(text("select id_data from sigl_dico_data where dico_name=:name and binary label=:label "
                                    "and binary code <=> :code order by id_data limit 1"),
                               {"name": d['dico_name'], "label": d['label'], "code": d['code']}).fetchone()
            if row:
                id_dico = row.id_data

        if not id_dico:
            res = conn.execute(text("insert into sigl_dico_data "
                                    "(id_owner, dico_name, label, short_label, position, code, dict_formatting) "
                                    "values (1, :dico_name, :label, :short_label, :position, :code, :dict_formatting)"),
                               d)
            id_dico = res.lastrowid

        dico_ids[d['ref']] = id_dico

    def dico(ref):
        return dico_ids[ref] if ref else None

    # Sampling acts first, LOINC analyses point to them by their code
    ana_ids = {}
    l_ana = sorted(data['analyses'], key=lambda a: a['cote_unite'] != 'PB')

    for a in l_ana:
        params = dict(a)
        params['famille'] = dico(a['famille'])
        params['type_prel'] = dico(a['type_prel'])
        params['type_analyse'] = dico(a['type_analyse'])
        params['produit_biologique'] = None

        if a['produit_biologique']:
            if a['produit_biologique'] in ana_ids:
                params['produit_biologique'] = ana_ids[a['produit_biologique']]
            else:
                row = conn.execute(text("select id_data from sigl_05_data where code=:code and cote_unite='PB'"),
                                   {"code": a['produit_biologique']}).fetchone()
                if row:
                    params['produit_biologique'] = row.id_data

        if a['cote_unite'] == 'PB':
            # Same act already created by the laboratory, or its code taken by another act
            row = conn.execute(text("select id_data from sigl_05_data where nom=:nom and cote_unite='PB'"),
                               {"nom": a['nom']}).fetchone()
            if row:
                ana_ids[a['code']] = row.id_data
                continue

            num = int(a['code'][2:])
            while conn.execute(text("select id_data from sigl_05_data where code=:code"),
                               {"code": 'PB' + str(num)}).fetchone():
                num += 1
            params['code'] = 'PB' + str(num)

        res = conn.execute(text("insert into sigl_05_data "
                                "(id_owner, code, nom, abbr, famille, cote_unite, cote_valeur, commentaire, "
                                "produit_biologique, type_prel, type_analyse, actif, ana_whonet, ana_ast, ana_loinc, "
                                "ana_lite) "
                                "values (:id_owner, :code, :nom, :abbr, :famille, :cote_unite, :cote_valeur, "
                                ":commentaire, :produit_biologique, :type_prel, :type_analyse, :actif, :ana_whonet, "
                                ":ana_ast, :ana_loinc, :ana_lite)"), params)
        ana_ids[a['code']] = res.lastrowid

    # Variables, code_var is the LOINC code or the code "en attente" of the ANS
    var_ids = {}

    for v in data['variables']:
        params = dict(v)
        params['unite'] = dico(v['unite'])
        params['unite2'] = dico(v['unite2'])
        params['type_resultat'] = dico(v['type_resultat'])

        if conn.execute(text("select id_data from sigl_07_data where code_var=:code_var"),
                        {"code_var": v['code_var']}).fetchone():
            print("WARNING code_var " + v['code_var'] + " already used, LOINC variable " + v['libelle'] +
                  " added with the same code_var")

        res = conn.execute(text("insert into sigl_07_data "
                                "(id_owner, libelle, description, unite, normal_min, normal_max, commentaire, "
                                "type_resultat, unite2, formule_unite2, formule, accuracy, precision2, code_var, "
                                "var_highlight, var_show_minmax, var_in_report) "
                                "values (1, :libelle, :description, :unite, :normal_min, :normal_max, :commentaire, "
                                ":type_resultat, :unite2, :formule_unite2, :formule, :accuracy, :precision2, "
                                ":code_var, :var_highlight, :var_show_minmax, :var_in_report)"), params)
        var_ids[v['code_var']] = res.lastrowid

    for code, code_var, position, num_var, oblig, var_whonet, var_qrcode, var_loinc in data['links']:
        conn.execute(text("insert into sigl_05_07_data "
                          "(id_owner, id_refanalyse, id_refvariable, position, num_var, obligatoire, var_whonet, "
                          "var_qrcode, var_loinc) "
                          "values (1, :id_ana, :id_var, :position, :num_var, :oblig, :var_whonet, :var_qrcode, "
                          ":var_loinc)"),
                     {"id_ana": ana_ids[code], "id_var": var_ids[code_var], "position": position,
                      "num_var": num_var, "oblig": oblig, "var_whonet": var_whonet, "var_qrcode": var_qrcode,
                      "var_loinc": var_loinc})

    print("LOINC repository added : " + str(len(ana_ids)) + " analyses, " + str(len(var_ids)) + " variables")


def fix_old_repository(conn, old_repo):
    """Each change checks the value of the demo base, a value changed by the laboratory is kept.
    Analyses and variables are found by code, ids differ from one base to another"""

    # Wrong or duplicate LOINC codes
    for code, old in old_repo['ana_loinc']:
        conn.execute(text("update sigl_05_data set ana_loinc='' where code=:code and ana_loinc=:old"),
                     {"code": code, "old": old})

    # Rating value entered by each laboratory
    for code, old in old_repo['cote_valeur']:
        conn.execute(text("update sigl_05_data set cote_valeur=0 where code=:code and cote_valeur=:old"),
                     {"code": code, "old": old})

    # Optional variables, the biologist checks the results are complete
    for code, code_var, old in old_repo['obligatoire']:
        conn.execute(text("update sigl_05_07_data l "
                          "join sigl_05_data a on a.id_data=l.id_refanalyse "
                          "join sigl_07_data v on v.id_data=l.id_refvariable "
                          "set l.obligatoire=5 where a.code=:code and v.code_var=:code_var "
                          "and l.obligatoire <=> :old"),
                     {"code": code, "code_var": code_var, "old": old})

    for code_var, old in old_repo['var_show_minmax']:
        conn.execute(text("update sigl_07_data set var_show_minmax='Y' "
                          "where code_var=:code_var and var_show_minmax <=> :old"),
                     {"code_var": code_var, "old": old})

    # Second unit : $ is the value entered, $_N gave a wrong value without error
    l_formula = [('4', '$_1*1.71', '$*1.71'), ('5', '$_1 * 1.7105', '$*1.7105'), ('6', '$_1 * 1.7105', '$*1.7105'),
                 ('11', '$_1 * 0.0249', '$*0.0249'), ('15', '$_1*17.92', '$*17.92'), ('27', '$_2*2.58', '$*2.58'),
                 ('28', '$_1 * 2.578', '$*2.578'), ('29', '$_1*2.58', '$*2.58'), ('30', '$_3*1.14', '$*1.14'),
                 ('31', '($_1 - $_2 - ($_3 / 5.6))*2.58', '$*2.58'), ('98', '$_1 * 0.00595', '$*0.00595'),
                 ('106', '$_1 * 5.551', '$*5.551'), ('109', '$_1 * 16.65', '$*16.65'),
                 ('110', '$_1 * 0.0249', '$*0.0249'), ('111', '$_1 * 0.0323', '$*0.0323'),
                 ('650', '$_1*5.551', '$*5.551')]

    for code_var, old, new in l_formula:
        conn.execute(text("update sigl_07_data set formule_unite2=:new "
                          "where code_var=:code_var and formule_unite2=:old"),
                     {"code_var": code_var, "old": old, "new": new})

    # NFS : a percentage to an absolute value needs the leucocytes, not possible as a second unit
    conn.execute(text("update sigl_07_data set unite2=NULL, formule_unite2=NULL, precision2=NULL "
                      "where code_var in ('160', '161', '162', '163', '164', '173', '174', '175', '176', '177') "
                      "and formule_unite2 like '$\\_4%'"))

    # Analyses without variable and not a sampling act : deleted, or deactivated if requested in a record
    l_ana = ['B011', 'B012', 'B028', 'B033', 'B034', 'B089', 'B098', 'B103', 'B109', 'B119', 'B120', 'B121',
             'B125', 'B127', 'B132', 'B133', 'B135', 'B140', 'B149', 'B158', 'B159', 'B160', 'B162', 'B169',
             'B173', 'B221', 'B225', 'B601', 'B700', 'NFR']

    for code in l_ana:
        row = conn.execute(text("select id_data from sigl_05_data where code=:code and cote_unite <> 'PB'"),
                           {"code": code}).fetchone()
        if not row:
            continue

        conn.execute(text("delete from sigl_05_data where id_data=:id "
                          "and not exists (select 1 from sigl_05_07_data l where l.id_refanalyse=:id) "
                          "and not exists (select 1 from sigl_04_data r where r.ref_analyse=:id) "
                          "and not exists (select 1 from (select produit_biologique from sigl_05_data) p "
                          "where p.produit_biologique=:id)"),
                     {"id": row.id_data})

        # Requested in a record : deactivated, the record stays readable
        conn.execute(text("update sigl_05_data set actif=5 where id_data=:id "
                          "and not exists (select 1 from sigl_05_07_data l where l.id_refanalyse=:id) "
                          "and not exists (select 1 from (select produit_biologique from sigl_05_data) p "
                          "where p.produit_biologique=:id)"),
                     {"id": row.id_data})

    # B136 rate of CD4 never computed
    conn.execute(text("update sigl_07_data set formule='$_1 / $_3 * 100' "
                      "where code_var='182' and formule='$1 / $3 * 100'"))

    # B072 Prolactine without type of result
    conn.execute(text("update sigl_07_data set type_resultat=228 "
                      "where code_var='89' and (type_resultat is null or type_resultat=0)"))

    # Unit million/mm3 twice, the second one merged into the first
    l_unit = conn.execute(text("select id_data from sigl_dico_data where dico_name='unite_valeur' "
                               "and binary label='million/mm3' order by id_data")).fetchall()
    if len(l_unit) == 2:
        keep, drop = l_unit[0].id_data, l_unit[1].id_data
        conn.execute(text("update sigl_07_data set unite=:keep where unite=:drop"), {"keep": keep, "drop": drop})
        conn.execute(text("update sigl_07_data set unite2=:keep where unite2=:drop"), {"keep": keep, "drop": drop})
        conn.execute(text("delete from sigl_dico_data where id_data=:drop"), {"drop": drop})

    # EPHU : Couleur behind Aspect
    conn.execute(text("update sigl_05_07_data l "
                      "join sigl_05_data a on a.id_data=l.id_refanalyse "
                      "join sigl_07_data v on v.id_data=l.id_refvariable "
                      "set l.position=25 where a.code='EPHU' and v.code_var='889' and l.position=20"))

    # DSQU : value "0" of code P1 is "+"
    conn.execute(text("update sigl_dico_data set label='+' where dico_name='DSQU' and code='P1' and label='0'"))


def sort_dictionaries(conn):
    # Units, families and types of sample in alphabetical order
    try:
        conn.execute(text("update sigl_dico_data d join ("
                          "select id_data, row_number() over (partition by dico_name order by label, id_data) * 10 "
                          "as new_pos from sigl_dico_data "
                          "where dico_name in ('unite_valeur', 'famille_analyse', 'type_prel')) t "
                          "on t.id_data=d.id_data set d.position=t.new_pos"))
    except Exception as err:
        print("ERROR sort units, families and types of sample,\n\terr=" + str(err))

    # Long lists of names : negative values first, then alphabetical order
    try:
        conn.execute(text("update sigl_dico_data d join ("
                          "select id_data, row_number() over (partition by dico_name order by "
                          "case when label like 'Néant%' or label like 'Absen%' or label like 'Négati%' "
                          "or label like 'Non identifi%' or label like 'AA (normal)%' then 0 else 1 end, "
                          "label, id_data) * 10 as new_pos from sigl_dico_data "
                          "where dico_name in ('bacterie', 'germe', 'cristaux', 'cylindre', 'gram', 'parasite', "
                          "'hbpheno')) t "
                          "on t.id_data=d.id_data set d.position=t.new_pos"))
    except Exception as err:
        print("ERROR sort lists of names,\n\terr=" + str(err))

    try:
        conn.execute(text("update sigl_dico_data d join ("
                          "select id_data, row_number() over (order by label, id_data) * 10 as new_pos "
                          "from sigl_dico_data where dico_name='type_resultat') t "
                          "on t.id_data=d.id_data set d.position=t.new_pos"))
    except Exception as err:
        print("ERROR sort types of result,\n\terr=" + str(err))


def downgrade():
    """
    No-op by design.

    This migration is intentionally irreversible per the organization's
    forward-only policy. To roll back, restore a verified backup
    taken before revision b2ef0260cddd.
    """
    print("downgrade skipped: irreversible migration b2ef0260cddd (forward-only policy)")
