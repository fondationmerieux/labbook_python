# -*- coding:utf-8 -*-
"""V3_5_3_user_signature

Revision ID: 14d207abf78f
Revises: 034e3ea3d81b
Create Date: 2025-01-29 17:11:37.803125

"""
from alembic import op
from sqlalchemy import text

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '14d207abf78f'
down_revision = '034e3ea3d81b'
branch_labels = None
depends_on = None


def upgrade():
    print("--- " + str(datetime.today()) + "---")
    print("START of migration V3_5_3_user_signature revision=14d207abf78f")

    # Get the current
    conn = op.get_bind()

    # Create table for user_signature_file
    try:
        conn.execute(text("create table user_signature_file("
                          "id_data INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                          "id_owner INT UNSIGNED DEFAULT NULL, "
                          "sys_creation_date DATETIME DEFAULT NULL, "
                          "sys_last_mod_date DATETIME DEFAULT NULL, "
                          "sys_last_mod_user INT UNSIGNED DEFAULT NULL, "
                          "id_ext INT UNSIGNED DEFAULT NULL, "
                          "id_file INT UNSIGNED DEFAULT NULL ) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table user_signature_file,\n\terr=" + str(err))

    # CHANGE COLUMN ans_lab28 to ans_connect
    try:
        conn.execute(text("alter table analyzer_setting change column ans_lab28 ans_connect varchar(255)"))
    except Exception as err:
        print("ERROR change column ans_lab28 to analyzer_setting,\n\terr=" + str(err))

    # Create table for storage_room
    try:
        conn.execute(text("create table storage_room("
                          "sro_ser int unsigned AUTO_INCREMENT PRIMARY KEY, "
                          "sro_date datetime, "
                          "sro_user int unsigned, "
                          "sro_name varchar(100) NOT NULL, "
                          "sro_abbrev varchar(10) NOT NULL UNIQUE, "
                          "sro_label varchar(10) NOT NULL ) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table storage_room,\n\terr=" + str(err))

    # Create table for storage_chamber
    try:
        conn.execute(text("create table storage_chamber("
                          "sch_ser int unsigned AUTO_INCREMENT PRIMARY KEY, "
                          "sch_date datetime, "
                          "sch_user int unsigned, "
                          "sch_room int unsigned NOT NULL, "
                          "sch_name varchar(100) NOT NULL, "
                          "sch_abbrev varchar(10) NOT NULL, "
                          "sch_label varchar(10) NOT NULL, "
                          "INDEX(sch_room)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table storage_chamber,\n\terr=" + str(err))

    # Create table for storage_compartment
    try:
        conn.execute(text("create table storage_compartment("
                          "sco_ser int unsigned AUTO_INCREMENT PRIMARY KEY, "
                          "sco_date datetime, "
                          "sco_user int unsigned, "
                          "sco_chamber int unsigned NOT NULL, "
                          "sco_name varchar(100) NOT NULL, "
                          "sco_abbrev varchar(10) NOT NULL, "
                          "sco_label varchar(10) NOT NULL, "
                          "sco_dim_x INT NOT NULL, "
                          "sco_dim_y INT NOT NULL, "
                          "sco_dim_z INT NOT NULL, "
                          "INDEX(sco_chamber)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table storage_compartment,\n\terr=" + str(err))

    # Create table for storage_box
    try:
        conn.execute(text("create table storage_box("
                          "sbo_ser INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, "
                          "sbo_date datetime, "
                          "sbo_user int unsigned, "
                          "sbo_compartment INT UNSIGNED NOT NULL, "
                          "sbo_name VARCHAR(100) NOT NULL, "
                          "sbo_label VARCHAR(10) NOT NULL,"
                          "sbo_coordinates VARCHAR(10) NOT NULL, "
                          "sbo_dim_x INT NOT NULL, "
                          "sbo_dim_y INT NOT NULL, "
                          "sbo_full VARCHAR(1) NOT NULL DEFAULT 'N', "
                          "INDEX(sbo_compartment)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table storage_box,\n\terr=" + str(err))

    # Create table for storage_aliquot
    # sal_type == type_prel from sigl_01_data
    # sal_patient > 0 if aliquot add outside of file
    try:
        conn.execute(text("create table storage_aliquot("
                          "sal_ser INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, "
                          "sal_date datetime, "
                          "sal_user int unsigned, "
                          "sal_sample INT UNSIGNED NOT NULL, "
                          "sal_patient INT UNSIGNED NOT NULL, "
                          "sal_type int unsigned NOT NULL, "
                          "sal_pathogen INT UNSIGNED NOT NULL,"
                          "sal_box INT UNSIGNED NOT NULL, "
                          "sal_coordinates VARCHAR(10) NOT NULL, "
                          "sal_in_stock VARCHAR(1) NOT NULL DEFAULT 'Y', "
                          "INDEX(sal_patient), INDEX(sal_patient), INDEX(sal_box)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table storage_aliquot,\n\terr=" + str(err))

    # Create table for sample_destock
    try:
        conn.execute(text("create table sample_destock("
                          "sad_ser INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, "
                          "sad_date datetime, "
                          "sad_user int unsigned, "
                          "sad_aliquot INT UNSIGNED NOT NULL, "
                          "sad_reason TEXT NOT NULL, "
                          "sad_external varchar(1) default 'N',"
                          "sad_location varchar(255) default '', "
                          "sad_destock_date datetime, "
                          "sad_restock_date datetime, "
                          "sad_restock_user int unsigned,"
                          "INDEX(sad_aliquot)) "
                          "character set=utf8"))
    except Exception as err:
        print("ERROR create table sample_destock,\n\terr=" + str(err))

    # insert bacteria pathogen dictionary
    try:
        conn.execute(text("INSERT INTO sigl_dico_data (id_owner, dico_name, label, short_label, position, code) VALUES "
                          "(0, 'pathogène', 'Actinomadura madurae', 'Actinomadura_madurae', 2, 'bact_1'),"
                          "(0, 'pathogène', 'Actinomadura pelletieri', 'Actinomadura', 3, 'bact_2'),"
                          "(0, 'pathogène', 'Actinomyces gerencseriae', 'Actinomyces', 4, 'bact_3'),"
                          "(0, 'pathogène', 'Actinomyces israelii', 'Actinomyces_israelii', 5, 'bact_4'),"
                          "(0, 'pathogène', 'Actinomyces spp.', 'Actinomyces_spp.', 6, 'bact_5'),"
                          "(0, 'pathogène', 'Aggregatibacter actinomycetemcomitans', 'Aggregatibacter', 7, 'bact_6'),"
                          "(0, 'pathogène', 'Anaplasma spp.', 'Anaplasma_spp.', 8, 'bact_7'),"
                          "(0, 'pathogène', 'Arcanobacterium haemolyticum', 'Arcanobacterium', 9, 'bact_8'),"
                          "(0, 'pathogène', 'Arcobacter butzleri', 'Arcobacter_butzleri', 10, 'bact_9'),"
                          "(0, 'pathogène', 'Bacillus anthracis', 'Bacillus_anthracis', 11, 'bact_10'),"
                          "(0, 'pathogène', 'Bacteroides fragilis', 'Bacteroides_fragilis', 12, 'bact_11'),"
                          "(0, 'pathogène', 'Bacteroides spp.', 'Bacteroides_spp.', 13, 'bact_12'),"
                          "(0, 'pathogène', 'Bartonella bacilliformis', 'Bartonella', 14, 'bact_13'),"
                          "(0, 'pathogène', 'Bartonella quintana', 'Bartonella_quintana', 15, 'bact_14'),"
                          "(0, 'pathogène', 'Bartonella spp.', 'Bartonella_spp.', 16, 'bact_15'),"
                          "(0, 'pathogène', 'Bordetella bronchiseptica', 'Bordetella', 17, 'bact_16'),"
                          "(0, 'pathogène', 'Bordetella parapertussis', 'Bordetella_2', 18, 'bact_17'),"
                          "(0, 'pathogène', 'Bordetella pertussis', 'Bordetella_pertussis', 19, 'bact_18'),"
                          "(0, 'pathogène', 'Bordetella spp.', 'Bordetella_spp.', 20, 'bact_19'),"
                          "(0, 'pathogène', 'Borrelia burgdorferi', 'Borrelia_burgdorferi', 21, 'bact_20'),"
                          "(0, 'pathogène', 'Borrelia duttonii', 'Borrelia_duttonii', 22, 'bact_21'),"
                          "(0, 'pathogène', 'Borrelia recurrentis', 'Borrelia_recurrentis', 23, 'bact_22'),"
                          "(0, 'pathogène', 'Borrelia spp.', 'Borrelia_spp.', 24, 'bact_23'),"
                          "(0, 'pathogène', 'Brachyspira spp.', 'Brachyspira_spp.', 25, 'bact_24'),"
                          "(0, 'pathogène', 'Brucella abortus', 'Brucella_abortus', 26, 'bact_25'),"
                          "(0, 'pathogène', 'Brucella canis', 'Brucella_canis', 27, 'bact_26'),"
                          "(0, 'pathogène', 'Brucella inopinata', 'Brucella_inopinata', 28, 'bact_27'),"
                          "(0, 'pathogène', 'Brucella melitensis', 'Brucella_melitensis', 29, 'bact_28'),"
                          "(0, 'pathogène', 'Brucella suis', 'Brucella_suis', 30, 'bact_29'),"
                          "(0, 'pathogène', 'Burkholderia cepacia', 'Burkholderia_cepacia', 31, 'bact_30'),"
                          "(0, 'pathogène', 'Burkholderia mallei', 'Burkholderia_mallei', 32, 'bact_31'),"
                          "(0, 'pathogène', 'Burkholderia pseudomallei', 'Burkholderia', 33, 'bact_32'),"
                          "(0, 'pathogène', 'Campylobacter fetus subsp. fetus', 'Campylobacter_fetus', 34, 'bact_33'),"
                          "(0, 'pathogène', 'Campylobacter fetus subsp. venerealis', 'Campylobacter_fetus_2', 35, 'bact_34'),"
                          "(0, 'pathogène', 'Campylobacter jejuni subsp. doylei', 'Campylobacter_jejuni', 36, 'bact_35'),"
                          "(0, 'pathogène', 'Campylobacter jejuni subsp. jejuni', 'Campylobacter_jejuni_2', 37, 'bact_36'),"
                          "(0, 'pathogène', 'Campylobacter spp.', 'Campylobacter_spp.', 38, 'bact_37'),"
                          "(0, 'pathogène', 'Cardiobacterium hominis', 'Cardiobacterium', 39, 'bact_38'),"
                          "(0, 'pathogène', 'Cardiobacterium valvarum', 'Cardiobacterium_2', 40, 'bact_39'),"
                          "(0, 'pathogène', 'Chlamydia abortus (Chlamydophila abortus)', 'Chlamydia_abortus', 41, 'bact_40'),"
                          "(0, 'pathogène', 'Chlamydia caviae (Chlamydophila caviae)', 'Chlamydia_caviae', 42, 'bact_41'),"
                          "(0, 'pathogène', 'Chlamydia felis (Chlamydophila felis)', 'Chlamydia_felis', 43, 'bact_42'),"
                          "(0, 'pathogène', 'Chlamydia pneumoniae (Chlamydophila pneumoniae)', 'Chlamydia_pneumoniae', 44, 'bact_43'),"
                          "(0, 'pathogène', 'Chlamydia psittaci (Chlamydophila psittaci) (souches aviaires)', 'Chlamydia_psittaci', 45, 'bact_44'),"
                          "(0, 'pathogène', 'Chlamydia psittaci (Chlamydophila psittaci) (autres souches)', 'Chlamydia_psittaci_2', 46, 'bact_45'),"
                          "(0, 'pathogène', 'Chlamydia trachomatis (Chlamydophila trachomatis)', 'Chlamydia', 47, 'bact_46'),"
                          "(0, 'pathogène', 'Clostridium botulinum', 'Clostridium', 48, 'bact_47'),"
                          "(0, 'pathogène', 'Clostridium difficile', 'Clostridium_2', 49, 'bact_48'),"
                          "(0, 'pathogène', 'Clostridium perfringens', 'Clostridium_3', 50, 'bact_49'),"
                          "(0, 'pathogène', 'Clostridium tetani', 'Clostridium_tetani', 51, 'bact_50'),"
                          "(0, 'pathogène', 'Clostridium spp.', 'Clostridium_spp.', 52, 'bact_51'),"
                          "(0, 'pathogène', 'Corynebacterium diphtheriae', 'Corynebacterium', 53, 'bact_52'),"
                          "(0, 'pathogène', 'Corynebacterium minutissimum', 'Corynebacterium_2', 54, 'bact_53'),"
                          "(0, 'pathogène', 'Corynebacterium pseudotuberculosis', 'Corynebacterium_3', 55, 'bact_54'),"
                          "(0, 'pathogène', 'Corynebacterium ulcerans', 'Corynebacterium_4', 56, 'bact_55'),"
                          "(0, 'pathogène', 'Corynebacterium spp.', 'Corynebacterium_spp.', 57, 'bact_56'),"
                          "(0, 'pathogène', 'Coxiella burnetii', 'Coxiella_burnetii', 58, 'bact_57'),"
                          "(0, 'pathogène', 'Edwardsiella tarda', 'Edwardsiella_tarda', 59, 'bact_58'),"
                          "(0, 'pathogène', 'Ehrlichia spp.', 'Ehrlichia_spp.', 60, 'bact_59'),"
                          "(0, 'pathogène', 'Eikenella corrodens', 'Eikenella_corrodens', 61, 'bact_60'),"
                          "(0, 'pathogène', 'Elizabethkingia meningoseptica (Flavobacterium meningosepticum)', 'Elizabethkingia', 62, 'bact_61'),"
                          "(0, 'pathogène', 'Enterobacter aerogenes (Klebsiella mobilis)', 'Enterobacter', 63, 'bact_62'),"
                          "(0, 'pathogène', 'Enterobacter cloacae subsp. cloacae (Enterobacter cloacae)', 'Enterobacter_cloacae', 64, 'bact_63'),"
                          "(0, 'pathogène', 'Enterobacter spp.', 'Enterobacter_spp.', 65, 'bact_64'),"
                          "(0, 'pathogène', 'Enterococcus spp.', 'Enterococcus_spp.', 66, 'bact_65'),"
                          "(0, 'pathogène', 'Erysipelothrix rhusiopathiae', 'Erysipelothrix', 67, 'bact_66'),"
                          "(0, 'pathogène', 'Escherichia coli (à l''exception des souches non pathogènes)', 'Escherichia_coli', 68, 'bact_67'),"
                          "(0, 'pathogène', 'Escherichia coli hautement pathogènes (E. coli entérohémorragiques (ECEH), entéro-invasifs (ECEI)entéropathogènes (ECEP), entérotoxinogènes (ECET), producteurs de shiga-toxines (STEC))', 'Escherichia_coli_2', 69, 'bact_68'),"
                          "(0, 'pathogène', 'Fluoribacter bozemanae (Legionella)', 'Fluoribacter', 70, 'bact_69'),"
                          "(0, 'pathogène', 'Francisella hispaniensis', 'Francisella', 71, 'bact_70'),"
                          "(0, 'pathogène', 'Francisella tularensis subsp. holarctica', 'Francisella_2', 72, 'bact_71'),"
                          "(0, 'pathogène', 'Francisella tularensis subsp. mediasiatica', 'Francisella_3', 73, 'bact_72'),"
                          "(0, 'pathogène', 'Francisella tularensis subsp. novicida', 'Francisella_4', 74, 'bact_73'),"
                          "(0, 'pathogène', 'Francisella tularensis subsp. tularensis', 'Francisella_5', 75, 'bact_74'),"
                          "(0, 'pathogène', 'Fusobacterium necrophorum subsp. funduliforme', 'Fusobacterium', 76, 'bact_75'),"
                          "(0, 'pathogène', 'Fusobacterium necrophorum subsp. necrophorum', 'Fusobacterium_2', 77, 'bact_76'),"
                          "(0, 'pathogène', 'Gardnerella vaginalis', 'Gardnerella', 78, 'bact_77'),"
                          "(0, 'pathogène', 'Haemophilus ducreyi', 'Haemophilus_ducreyi', 79, 'bact_78'),"
                          "(0, 'pathogène', 'Haemophilus influenzae', 'Haemophilus', 80, 'bact_79'),"
                          "(0, 'pathogène', 'Haemophilus spp.', 'Haemophilus_spp.', 81, 'bact_80'),"
                          "(0, 'pathogène', 'Helicobacter pylori', 'Helicobacter_pylori', 82, 'bact_81'),"
                          "(0, 'pathogène', 'Helicobacter spp.', 'Helicobacter_spp.', 83, 'bact_82'),"
                          "(0, 'pathogène', 'Klebsiella oxytoca', 'Klebsiella_oxytoca', 84, 'bact_83'),"
                          "(0, 'pathogène', 'Klebsiella pneumoniae subsp. ozaenae', 'Klebsiella', 85, 'bact_84'),"
                          "(0, 'pathogène', 'Klebsiella pneumoniae subsp. pneumoniae', 'Klebsiella_2', 86, 'bact_85'),"
                          "(0, 'pathogène', 'Klebsiella pneumoniae subsp. rhinoscleromatis', 'Klebsiella_3', 87, 'bact_86'),"
                          "(0, 'pathogène', 'Klebsiella spp.', 'Klebsiella_spp.', 88, 'bact_87'),"
                          "(0, 'pathogène', 'Legionella pneumophila subsp. fraseri', 'Legionella', 89, 'bact_88'),"
                          "(0, 'pathogène', 'Legionella pneumophila subsp. pascullei', 'Legionella_2', 90, 'bact_89'),"
                          "(0, 'pathogène', 'Legionella pneumophila subsp. pneumophila', 'Legionella_3', 91, 'bact_90'),"
                          "(0, 'pathogène', 'Legionella spp.', 'Legionella_spp.', 92, 'bact_91'),"
                          "(0, 'pathogène', 'Leptospira interrogans icterohemorrhagiae', 'Leptospira', 93, 'bact_92'),"
                          "(0, 'pathogène', 'Leptospira interrogans (tous serovars)', 'Leptospira_2', 94, 'bact_93'),"
                          "(0, 'pathogène', 'Leptospira interrogans spp.', 'Leptospira_3', 95, 'bact_94'),"
                          "(0, 'pathogène', 'Listeria monocytogenes', 'Listeria', 96, 'bact_95'),"
                          "(0, 'pathogène', 'Listeria ivanovii subsp. ivanovii', 'Listeria_ivanovii', 97, 'bact_96'),"
                          "(0, 'pathogène', 'Listeria ivanovii subsp. londoniensis', 'Listeria_ivanovii_2', 98, 'bact_97'),"
                          "(0, 'pathogène', 'Morganella morganii subsp. morganii', 'Morganella_morganii', 99, 'bact_98'),"
                          "(0, 'pathogène', 'Morganella morganii subsp. sibonii', 'Morganella_morganii_2', 100, 'bact_99'),"
                          "(0, 'pathogène', 'Mycobacterium tuberculosis complex, Mycobacterium africanum', 'Mycobacterium', 101, 'bact_100'),"
                          "(0, 'pathogène', 'Mycobacterium tuberculosis complex, Mycobacterium bovis', 'Mycobacterium_2', 102, 'bact_101'),"
                          "(0, 'pathogène', 'Mycobacterium tuberculosis complex, Mycobacterium caprae', 'Mycobacterium_3', 103, 'bact_102'),"
                          "(0, 'pathogène', 'Mycobacterium tuberculosis complex, Mycobacterium microti', 'Mycobacterium_4', 104, 'bact_103'),"
                          "(0, 'pathogène', 'Mycobacterium tuberculosis complex, Mycobacterium pinnipedii', 'Mycobacterium_5', 105, 'bact_104'),"
                          "(0, 'pathogène', 'Mycobacterium tuberculosis complex, Mycobacterium tuberculosis', 'Mycobacterium_6', 106, 'bact_105'),"
                          "(0, 'pathogène', 'Mycobacterium abscessus subsp. abscessus', 'Mycobacterium_7', 107, 'bact_106'),"
                          "(0, 'pathogène', 'Mycobacterium avium complex, Mycobacterium avium', 'Mycobacterium_avium', 108, 'bact_107'),"
                          "(0, 'pathogène', 'Mycobacterium avium complex, Mycobacterium paratuberculosis', 'Mycobacterium_avium_2', 109, 'bact_108'),"
                          "(0, 'pathogène', 'Mycobacterium avium complex, Mycobacterium chimaera', 'Mycobacterium_avium_3', 110, 'bact_109'),"
                          "(0, 'pathogène', 'Mycobacterium avium complex, Mycobacterium intracellulare', 'Mycobacterium_avium_4', 111, 'bact_110'),"
                          "(0, 'pathogène', 'Mycobacterium avium complex, Mycobacterium silvaticum', 'Mycobacterium_avium_5', 112, 'bact_111'),"
                          "(0, 'pathogène', 'Mycobacterium chelonae', 'Mycobacterium_8', 113, 'bact_112'),"
                          "(0, 'pathogène', 'Mycobacterium fortuitum complex, Mycobacterium fortuitum', 'Mycobacterium_9', 114, 'bact_113'),"
                          "(0, 'pathogène', 'Mycobacterium kansasii', 'Mycobacterium_10', 115, 'bact_114'),"
                          "(0, 'pathogène', 'Mycobacterium leprae', 'Mycobacterium_leprae', 116, 'bact_115'),"
                          "(0, 'pathogène', 'Mycobacterium malmoense', 'Mycobacterium_11', 117, 'bact_116'),"
                          "(0, 'pathogène', 'Mycobacterium marinum', 'Mycobacterium_12', 118, 'bact_117'),"
                          "(0, 'pathogène', 'Mycobacterium scrofulaceum', 'Mycobacterium_13', 119, 'bact_118'),"
                          "(0, 'pathogène', 'Mycobacterium simiae complex, Mycobacterium simiae', 'Mycobacterium_simiae', 120, 'bact_119'),"
                          "(0, 'pathogène', 'Mycobacterium szulgai', 'Mycobacterium_14', 121, 'bact_120'),"
                          "(0, 'pathogène', 'Mycobacterium ulcerans', 'Mycobacterium_15', 122, 'bact_121'),"
                          "(0, 'pathogène', 'Mycobacterium xenopi', 'Mycobacterium_xenopi', 123, 'bact_122'),"
                          "(0, 'pathogène', 'Mycoplasma hominis', 'Mycoplasma_hominis', 124, 'bact_123'),"
                          "(0, 'pathogène', 'Mycoplasma pneumoniae', 'Mycoplasma', 125, 'bact_124'),"
                          "(0, 'pathogène', 'Mycoplasma spp.', 'Mycoplasma_spp.', 126, 'bact_125'),"
                          "(0, 'pathogène', 'Neisseria gonorrhoeae', 'Neisseria', 127, 'bact_126'),"
                          "(0, 'pathogène', 'Neisseria meningitidis', 'Neisseria_2', 128, 'bact_127'),"
                          "(0, 'pathogène', 'Neorickettsia sennetsu (Rickettsia sennetsu, Ehrlichia sennetsu)', 'Neorickettsia', 129, 'bact_128'),"
                          "(0, 'pathogène', 'Nocardia asteroides', 'Nocardia_asteroides', 130, 'bact_129'),"
                          "(0, 'pathogène', 'Nocardia brasiliensis', 'Nocardia', 131, 'bact_130'),"
                          "(0, 'pathogène', 'Nocardia farcinica', 'Nocardia_farcinica', 132, 'bact_131'),"
                          "(0, 'pathogène', 'Nocardia nova', 'Nocardia_nova', 133, 'bact_132'),"
                          "(0, 'pathogène', 'Nocardia otitidiscaviarum', 'Nocardia_2', 134, 'bact_133'),"
                          "(0, 'pathogène', 'Nocardia spp.', 'Nocardia_spp.', 135, 'bact_134'),"
                          "(0, 'pathogène', 'Orientia tsutsugamushi (Rickettsia tsutsugamushi)', 'Orientia', 136, 'bact_135'),"
                          "(0, 'pathogène', 'Pasteurella multocida subsp. gallicida (Pasteurella gallicida)', 'Pasteurella', 137, 'bact_136'),"
                          "(0, 'pathogène', 'Pasteurella multocida subsp. multocida', 'Pasteurella_2', 138, 'bact_137'),"
                          "(0, 'pathogène', 'Pasteurella multocida subsp. septica', 'Pasteurella_3', 139, 'bact_138'),"
                          "(0, 'pathogène', 'Pasteurella spp.', 'Pasteurella_spp.', 140, 'bact_139'),"
                          "(0, 'pathogène', 'Peptostreptococcus anaerobius', 'Peptostreptococcus', 141, 'bact_140'),"
                          "(0, 'pathogène', 'Plesiomonas shigelloides', 'Plesiomonas', 142, 'bact_141'),"
                          "(0, 'pathogène', 'Porphyromonas spp.', 'Porphyromonas_spp.', 143, 'bact_142'),"
                          "(0, 'pathogène', 'Prevotella spp.', 'Prevotella_spp.', 144, 'bact_143'),"
                          "(0, 'pathogène', 'Proteus mirabilis', 'Proteus_mirabilis', 145, 'bact_144'),"
                          "(0, 'pathogène', 'Proteus penneri', 'Proteus_penneri', 146, 'bact_145'),"
                          "(0, 'pathogène', 'Proteus vulgaris', 'Proteus_vulgaris', 147, 'bact_146'),"
                          "(0, 'pathogène', 'Providencia alcalifaciens', 'Providencia', 148, 'bact_147'),"
                          "(0, 'pathogène', 'Providencia rettgeri', 'Providencia_rettgeri', 149, 'bact_148'),"
                          "(0, 'pathogène', 'Providencia spp.', 'Providencia_spp.', 150, 'bact_149'),"
                          "(0, 'pathogène', 'Pseudomonas aeruginosa', 'Pseudomonas', 151, 'bact_150'),"
                          "(0, 'pathogène', 'Rhodococcus hoagii', 'Rhodococcus_hoagii', 152, 'bact_151'),"
                          "(0, 'pathogène', 'Rickettsia africae', 'Rickettsia_africae', 153, 'bact_152'),"
                          "(0, 'pathogène', 'Rickettsia akari', 'Rickettsia_akari', 154, 'bact_153'),"
                          "(0, 'pathogène', 'Rickettsia australis', 'Rickettsia_australis', 155, 'bact_154'),"
                          "(0, 'pathogène', 'Rickettsia canadensis', 'Rickettsia', 156, 'bact_155'),"
                          "(0, 'pathogène', 'Rickettsia conorii', 'Rickettsia_conorii', 157, 'bact_156'),"
                          "(0, 'pathogène', 'Rickettsia heilongjiangensis', 'Rickettsia_2', 158, 'bact_157'),"
                          "(0, 'pathogène', 'Rickettsia japonica', 'Rickettsia_japonica', 159, 'bact_158'),"
                          "(0, 'pathogène', 'Rickettsia montanensis', 'Rickettsia_3', 160, 'bact_159'),"
                          "(0, 'pathogène', 'Rickettsia typhi', 'Rickettsia_typhi', 161, 'bact_160'),"
                          "(0, 'pathogène', 'Rickettsia prowazekii', 'Rickettsia_4', 162, 'bact_161'),"
                          "(0, 'pathogène', 'Rickettsia rickettsii', 'Rickettsia_5', 163, 'bact_162'),"
                          "(0, 'pathogène', 'Rickettsia sibirica', 'Rickettsia_sibirica', 164, 'bact_163'),"
                          "(0, 'pathogène', 'Rickettsia spp.', 'Rickettsia_spp.', 165, 'bact_164'),"
                          "(0, 'pathogène', 'Salmonella enterica (choleraesuis) subsp. arizonae', 'Salmonella_enterica', 166, 'bact_165'),"
                          "(0, 'pathogène', 'Salmonella Enteritidis', 'Salmonella', 167, 'bact_166'),"
                          "(0, 'pathogène', 'Salmonella Paratyphi A, B, C', 'Salmonella_Paratyphi', 168, 'bact_167'),"
                          "(0, 'pathogène', 'Salmonella Typhi', 'Salmonella_Typhi', 169, 'bact_168'),"
                          "(0, 'pathogène', 'Salmonella Typhimurium', 'Salmonella_2', 170, 'bact_169'),"
                          "(0, 'pathogène', 'Salmonella (autres serovars)', 'Salmonella_3', 171, 'bact_170'),"
                          "(0, 'pathogène', 'Shigella boydii', 'Shigella_boydii', 172, 'bact_171'),"
                          "(0, 'pathogène', 'Shigella dysenteriae (Type 1)', 'Shigella_dysenteriae', 173, 'bact_172'),"
                          "(0, 'pathogène', 'Shigella dysenteriae (autre que le Type 1)', 'Shigella_dysenteriae_2', 174, 'bact_173'),"
                          "(0, 'pathogène', 'Shigella flexneri', 'Shigella_flexneri', 175, 'bact_174'),"
                          "(0, 'pathogène', 'Shigella sonnei', 'Shigella_sonnei', 176, 'bact_175'),"
                          "(0, 'pathogène', 'Staphylococcus aureus', 'Staphylococcus', 177, 'bact_176'),"
                          "(0, 'pathogène', 'Streptobacillus moniliformis', 'Streptobacillus', 178, 'bact_177'),"
                          "(0, 'pathogène', 'Streptococcus agalactiae', 'Streptococcus', 179, 'bact_178'),"
                          "(0, 'pathogène', 'Streptococcus dysgalactiae subsp. equisimilis', 'Streptococcus_2', 180, 'bact_179'),"
                          "(0, 'pathogène', 'Streptococcus pneumoniae', 'Streptococcus_3', 181, 'bact_180'),"
                          "(0, 'pathogène', 'Streptococcus pyogenes', 'Streptococcus_4', 182, 'bact_181'),"
                          "(0, 'pathogène', 'Streptococcus suis', 'Streptococcus_suis', 183, 'bact_182'),"
                          "(0, 'pathogène', 'Streptococcus spp.', 'Streptococcus_spp.', 184, 'bact_183'),"
                          "(0, 'pathogène', 'Treponema carateum', 'Treponema_carateum', 185, 'bact_184'),"
                          "(0, 'pathogène', 'Treponema pallidum', 'Treponema_pallidum', 186, 'bact_185'),"
                          "(0, 'pathogène', 'Treponema pertenue', 'Treponema_pertenue', 187, 'bact_186'),"
                          "(0, 'pathogène', 'Treponema spp.', 'Treponema_spp.', 188, 'bact_187'),"
                          "(0, 'pathogène', 'Trueperella pyogenes', 'Trueperella_pyogenes', 189, 'bact_188'),"
                          "(0, 'pathogène', 'Ureaplasma parvum', 'Ureaplasma_parvum', 190, 'bact_189'),"
                          "(0, 'pathogène', 'Ureaplasma urealyticum', 'Ureaplasma', 191, 'bact_190'),"
                          "(0, 'pathogène', 'Vibrio cholerae', 'Vibrio_cholerae', 192, 'bact_191'),"
                          "(0, 'pathogène', 'Vibrio parahaemolyticus', 'Vibrio', 193, 'bact_192'),"
                          "(0, 'pathogène', 'Vibrio spp.', 'Vibrio_spp.', 194, 'bact_193'),"
                          "(0, 'pathogène', 'Yersinia enterocolitica subsp. enterolitica', 'Yersinia', 195, 'bact_194'),"
                          "(0, 'pathogène', 'Yersinia enterocolitica subsp. palearctica', 'Yersinia_2', 196, 'bact_195'),"
                          "(0, 'pathogène', 'Yersinia pestis', 'Yersinia_pestis', 197, 'bact_196'),"
                          "(0, 'pathogène', 'Yersinia pseudotuberculosis', 'Yersinia_3', 198, 'bact_197'),"
                          "(0, 'pathogène', 'Yersinia spp.', 'Yersinia_spp.', 199, 'bact_198')"))
    except Exception as err:
        print("ERROR insert 198 bacteria pathogen dictionary,\n\terr=" + str(err))

    # insert 248 virus pathogen dictionary
    try:
        conn.execute(text("INSERT INTO sigl_dico_data (id_owner, dico_name, label, short_label, position, code) VALUES "
                          "(0, 'pathogène', 'Arenaviridae ', 'Arenaviridae', 200, 'virus_1'),"
                          "(0, 'pathogène', 'Mammarenavirus ', 'Mammarenavirus', 201, 'virus_2'),"
                          "(0, 'pathogène', 'Brazilian mammarenavirus (virus Sabiá)', 'Brazilian', 202, 'virus_3'),"
                          "(0, 'pathogène', 'Chapare mammarenavirus', 'Chapare', 203, 'virus_4'),"
                          "(0, 'pathogène', 'Flexal mammarenavirus', 'Flexal', 204, 'virus_5'),"
                          "(0, 'pathogène', 'Guanarito mammarenavirus', 'Guanarito', 205, 'virus_6'),"
                          "(0, 'pathogène', 'Argentinian mammarenavirus (virus Junín)', 'Argentinian', 206, 'virus_7'),"
                          "(0, 'pathogène', 'Lassa mammarenavirus', 'Lassa_mammarenavirus', 207, 'virus_8'),"
                          "(0, 'pathogène', 'Lujo mammarenavirus', 'Lujo_mammarenavirus', 208, 'virus_9'),"
                          "(0, 'pathogène', 'Lymphocytic choriomeningitis mammarenavirus (souches neurotropes)', 'Lymphocytic', 209, 'virus_10'),"
                          "(0, 'pathogène', 'Lymphocytic choriomeningitis mammarenavirus (autres souches)', 'Lymphocytic_2', 210, 'virus_11'),"
                          "(0, 'pathogène', 'Machupo mammarenavirus', 'Machupo', 211, 'virus_12'),"
                          "(0, 'pathogène', 'Mobala mammarenavirus', 'Mobala', 212, 'virus_13'),"
                          "(0, 'pathogène', 'Mopeia mammarenavirus', 'Mopeia', 213, 'virus_14'),"
                          "(0, 'pathogène', 'Tacaribe mammarenavirus', 'Tacaribe', 214, 'virus_15'),"
                          "(0, 'pathogène', 'Whitewater Arroyo mammarenavirus', 'Whitewater_Arroyo', 215, 'virus_16'),"
                          "(0, 'pathogène', 'Hantaviridae ', 'Hantaviridae', 216, 'virus_17'),"
                          "(0, 'pathogène', 'Orthohantavirus ', 'Orthohantavirus', 217, 'virus_18'),"
                          "(0, 'pathogène', 'Andes orthohantavirus (virus causant le syndrome pulmonaire à hantavirus [SPH])', 'Andes', 218, 'virus_19'),"
                          "(0, 'pathogène', 'Bayou orthohantavirus', 'Bayou', 219, 'virus_20'),"
                          "(0, 'pathogène', 'Black Creek Canal orthohantavirus', 'Black_Creek_Canal', 220, 'virus_21'),"
                          "(0, 'pathogène', 'Cano Delgadito orthohantavirus', 'Cano_Delgadito', 221, 'virus_22'),"
                          "(0, 'pathogène', 'Choclo orthohantavirus', 'Choclo', 222, 'virus_23'),"
                          "(0, 'pathogène', 'Dobrava-Belgrade orthohantavirus (virus causant la fièvre hémorragique avec syndrome rénal [FHSR])', 'Dobrava-Belgrade', 223, 'virus_24'),"
                          "(0, 'pathogène', 'El Moro Canyon orthohantavirus', 'El_Moro_Canyon', 224, 'virus_25'),"
                          "(0, 'pathogène', 'Hantaan orthohantavirus (virus causant la fièvre hémorragique avec syndrome rénal [FHSR])', 'Hantaan', 225, 'virus_26'),"
                          "(0, 'pathogène', 'Laguna Negra orthohantavirus', 'Laguna_Negra', 226, 'virus_27'),"
                          "(0, 'pathogène', 'Prospect Hill orthohantavirus', 'Prospect_Hill', 227, 'virus_28'),"
                          "(0, 'pathogène', 'Puumala orthohantavirus (virus causant la néphropathie épidémique scandinave [NE])', 'Puumala', 228, 'virus_29'),"
                          "(0, 'pathogène', 'Seoul orthohantavirus (virus causant la fièvre hémorragique avec syndrome rénal [FHSR])', 'Seoul', 229, 'virus_30'),"
                          "(0, 'pathogène', 'Sin Nombre orthohantavirus (virus causant le syndrome pulmonaire à hantavirus [SPH])', 'Sin_Nombre', 230, 'virus_31'),"
                          "(0, 'pathogène', 'Autres Orthohantavirus connus pour être pathogènes', 'Autres', 231, 'virus_32'),"
                          "(0, 'pathogène', 'Nairoviridae ', 'Nairoviridae', 232, 'virus_33'),"
                          "(0, 'pathogène', 'Orthonairovirus ', 'Orthonairovirus', 233, 'virus_34'),"
                          "(0, 'pathogène', 'Crimean-Congo hemorrhagic fever orthonairovirus', 'Crimean-Congo', 234, 'virus_35'),"
                          "(0, 'pathogène', 'Dugbe orthonairovirus', 'Dugbe', 235, 'virus_36'),"
                          "(0, 'pathogène', 'Hazara orthonairovirus', 'Hazara', 236, 'virus_37'),"
                          "(0, 'pathogène', 'Nairobi sheep disease orthonairovirus', 'Nairobi_sheep', 237, 'virus_38'),"
                          "(0, 'pathogène', 'Autres Orthonairovirus connus pour être pathogènes', 'Autres_2', 238, 'virus_39'),"
                          "(0, 'pathogène', 'Peribunyaviridae ', 'Peribunyaviridae', 239, 'virus_40'),"
                          "(0, 'pathogène', 'Orthobunyavirus ', 'Orthobunyavirus', 240, 'virus_41'),"
                          "(0, 'pathogène', 'Bunyamwera orthobunyavirus (virus Germiston)', 'Bunyamwera', 241, 'virus_42'),"
                          "(0, 'pathogène', 'California encephalitis orthobunyavirus', 'California', 242, 'virus_43'),"
                          "(0, 'pathogène', 'Oropouche orthobunyavirus', 'Oropouche', 243, 'virus_44'),"
                          "(0, 'pathogène', 'Autres orthobunyavirus connus pour être pathogènes', 'Autres_3', 244, 'virus_45'),"
                          "(0, 'pathogène', 'Phenuiviridae ', 'Phenuiviridae', 245, 'virus_46'),"
                          "(0, 'pathogène', 'Bandavirus ', 'Bandavirus', 246, 'virus_47'),"
                          "(0, 'pathogène', 'Bhanja bandavirus', 'Bhanja_bandavirus', 247, 'virus_48'),"
                          "(0, 'pathogène', 'Dabie bandavirus (virus du syndrome de fièvre sévère avec thrombocytopénie [SFTS])', 'Dabie_bandavirus', 248, 'virus_49'),"
                          "(0, 'pathogène', 'Phlebovirus ', 'Phlebovirus', 249, 'virus_50'),"
                          "(0, 'pathogène', 'Naples phlebovirus', 'Naples_phlebovirus', 250, 'virus_51'),"
                          "(0, 'pathogène', 'Punta Toro phlebovirus', 'Punta_Toro', 251, 'virus_52'),"
                          "(0, 'pathogène', 'Rift Valley fever phlebovirus', 'Rift_Valley_fever', 252, 'virus_53'),"
                          "(0, 'pathogène', 'Toscana phlebovirus', 'Toscana_phlebovirus', 253, 'virus_54'),"
                          "(0, 'pathogène', 'Autres phlebovirus connus pour être pathogènes', 'Autres_phlebovirus', 254, 'virus_55'),"
                          "(0, 'pathogène', 'Herpesviridae ', 'Herpesviridae', 255, 'virus_56'),"
                          "(0, 'pathogène', 'Cytomegalovirus ', 'Cytomegalovirus', 256, 'virus_57'),"
                          "(0, 'pathogène', 'Human betaherpesvirus 5 (cytomegalovirus)', 'Human', 257, 'virus_58'),"
                          "(0, 'pathogène', 'Lymphocryptovirus ', 'Lymphocryptovirus', 258, 'virus_59'),"
                          "(0, 'pathogène', 'Human gammaherpesvirus 4 (virus d''Epstein-Barr)', 'Human_2', 259, 'virus_60'),"
                          "(0, 'pathogène', 'Rhadinovirus ', 'Rhadinovirus', 260, 'virus_61'),"
                          "(0, 'pathogène', 'Human gammaherpesvirus 8', 'Human_3', 261, 'virus_62'),"
                          "(0, 'pathogène', 'Roseolovirus ', 'Roseolovirus', 262, 'virus_63'),"
                          "(0, 'pathogène', 'Human betaherpesvirus 6A (virus lymphotrope B humain)', 'Human_4', 263, 'virus_64'),"
                          "(0, 'pathogène', 'Human betaherpesvirus 6B', 'Human_5', 264, 'virus_65'),"
                          "(0, 'pathogène', 'Human betaherpesvirus 7', 'Human_6', 265, 'virus_66'),"
                          "(0, 'pathogène', 'Simplexvirus ', 'Simplexvirus', 266, 'virus_67'),"
                          "(0, 'pathogène', 'Macacine alphaherpesvirus 1 (herpesvirus simiae, virus Herpes B)', 'Macacine', 267, 'virus_68'),"
                          "(0, 'pathogène', 'Human alphaherpesvirus 1 (herpesvirus humain 1, virus Herpes simplex de type 1)', 'Human_7', 268, 'virus_69'),"
                          "(0, 'pathogène', 'Human alphaherpesvirus 2 (herpesvirus humain 2, virus Herpes simplex de type 2)', 'Human_8', 269, 'virus_70'),"
                          "(0, 'pathogène', 'Varicellovirus ', 'Varicellovirus', 270, 'virus_71'),"
                          "(0, 'pathogène', 'Human alphaherpesvirus 3 (herpesvirus varicella-zoster)', 'Human_9', 271, 'virus_72'),"
                          "(0, 'pathogène', 'Filoviridae ', 'Filoviridae', 272, 'virus_73'),"
                          "(0, 'pathogène', 'Ebolavirus ', 'Ebolavirus', 273, 'virus_74'),"
                          "(0, 'pathogène', 'Marburgvirus ', 'Marburgvirus', 274, 'virus_75'),"
                          "(0, 'pathogène', 'Marburg marburgvirus', 'Marburg_marburgvirus', 275, 'virus_76'),"
                          "(0, 'pathogène', 'Paramyxoviridae ', 'Paramyxoviridae', 276, 'virus_77'),"
                          "(0, 'pathogène', 'Orthoavulavirus ', 'Orthoavulavirus', 277, 'virus_78'),"
                          "(0, 'pathogène', 'Avian orthoavulavirus 1 (virus de la maladie de Newcastle)', 'Avian', 278, 'virus_79'),"
                          "(0, 'pathogène', 'Henipavirus ', 'Henipavirus', 279, 'virus_80'),"
                          "(0, 'pathogène', 'Hendra henipavirus', 'Hendra_henipavirus', 280, 'virus_81'),"
                          "(0, 'pathogène', 'Nipah henipavirus', 'Nipah_henipavirus', 281, 'virus_82'),"
                          "(0, 'pathogène', 'Morbillivirus ', 'Morbillivirus', 282, 'virus_83'),"
                          "(0, 'pathogène', 'Measles morbillivirus (virus de la rougeole)', 'Measles', 283, 'virus_84'),"
                          "(0, 'pathogène', 'Respirovirus ', 'Respirovirus', 284, 'virus_85'),"
                          "(0, 'pathogène', 'Human respirovirus 1 (virus para-influenza de type 1)', 'Human_respirovirus_1', 285, 'virus_86'),"
                          "(0, 'pathogène', 'Human respirovirus 3 (virus para-influenza de type 3)', 'Human_respirovirus_3', 286, 'virus_87'),"
                          "(0, 'pathogène', 'Othorubulavirus ', 'Othorubulavirus', 287, 'virus_88'),"
                          "(0, 'pathogène', 'Mumps orthorubulavirus (virus des oreillons)', 'Mumps', 288, 'virus_89'),"
                          "(0, 'pathogène', 'Human orthorubulavirus 2 (virus para-influenza de type 2)', 'Human_10', 289, 'virus_90'),"
                          "(0, 'pathogène', 'Human orthorubulavirus 4 (virus para-influenza de type 4)', 'Human_11', 290, 'virus_91'),"
                          "(0, 'pathogène', 'Pneumoviridae ', 'Pneumoviridae', 291, 'virus_92'),"
                          "(0, 'pathogène', 'Metapneumovirus ', 'Metapneumovirus', 292, 'virus_93'),"
                          "(0, 'pathogène', 'Orthopneumovirus ', 'Orthopneumovirus', 293, 'virus_94'),"
                          "(0, 'pathogène', 'Human orthopneumovirus (virus respiratoire syncytial)', 'Human_12', 294, 'virus_95'),"
                          "(0, 'pathogène', 'Rhabdoviridae ', 'Rhabdoviridae', 295, 'virus_96'),"
                          "(0, 'pathogène', 'Lyssavirus ', 'Lyssavirus', 296, 'virus_97'),"
                          "(0, 'pathogène', 'Australian bat lyssavirus', 'Australian_bat', 297, 'virus_98'),"
                          "(0, 'pathogène', 'Duvenhage lyssavirus', 'Duvenhage_lyssavirus', 298, 'virus_99'),"
                          "(0, 'pathogène', 'European bat 1 lyssavirus', 'European_bat_1', 299, 'virus_100'),"
                          "(0, 'pathogène', 'European bat 2 lyssavirus', 'European_bat_2', 300, 'virus_101'),"
                          "(0, 'pathogène', 'Lagos bat lyssavirus', 'Lagos_bat_lyssavirus', 301, 'virus_102'),"
                          "(0, 'pathogène', 'Mokola lyssavirus', 'Mokola_lyssavirus', 302, 'virus_103'),"
                          "(0, 'pathogène', 'Rabies lyssavirus (virus de la rage)', 'Rabies_lyssavirus', 303, 'virus_104'),"
                          "(0, 'pathogène', 'Vesiculovirus ', 'Vesiculovirus', 304, 'virus_105'),"
                          "(0, 'pathogène', 'Alagoas vesiculovirus (virus de la stomatite vésiculeuse)', 'Alagoas', 305, 'virus_106'),"
                          "(0, 'pathogène', 'Indiana vesiculovirus (virus de la stomatite vésiculeuse)', 'Indiana', 306, 'virus_107'),"
                          "(0, 'pathogène', 'New Jersey vesiculovirus (virus de la stomatite vésiculeuse)', 'New_Jersey', 307, 'virus_108'),"
                          "(0, 'pathogène', 'Piry vesiculovirus (virus Piry)', 'Piry_vesiculovirus', 308, 'virus_109'),"
                          "(0, 'pathogène', 'Coronaviridae ', 'Coronaviridae', 309, 'virus_110'),"
                          "(0, 'pathogène', 'Betacoronavirus ', 'Betacoronavirus', 310, 'virus_111'),"
                          "(0, 'pathogène', 'Severe acute respiratory syndrome-related coronavirus (coronavirus lié au syndrome aigu respiratoire sévère [virus SARS-CoV])', 'Severe_acute', 311, 'virus_112'),"
                          "(0, 'pathogène', 'Severe acute respiratory syndrome-related coronavirus-2 (coronavirus lié au syndrome aigu respiratoire sévère [virus SARS-CoV-2])', 'Severe_acute_2', 312, 'virus_113'),"
                          "(0, 'pathogène', 'Middle East respiratory syndrome-related coronavirus (coronavirus du syndrome respiratoire du Moyen-Orient [virus MERS-CoV])', 'Middle_East', 313, 'virus_114'),"
                          "(0, 'pathogène', 'Autres Coronaviridae connus pour être pathogènes', 'Autres_Coronaviridae', 314, 'virus_115'),"
                          "(0, 'pathogène', 'Caliciviridae ', 'Caliciviridae', 315, 'virus_116'),"
                          "(0, 'pathogène', 'Norovirus ', 'Norovirus', 316, 'virus_117'),"
                          "(0, 'pathogène', 'Norwalk virus', 'Norwalk_virus', 317, 'virus_118'),"
                          "(0, 'pathogène', 'Autres Caliciviridae connus pour être pathogènes', 'Autres_Caliciviridae', 318, 'virus_119'),"
                          "(0, 'pathogène', 'Picornaviridae ', 'Picornaviridae', 319, 'virus_120'),"
                          "(0, 'pathogène', 'Cardiovirus ', 'Cardiovirus', 320, 'virus_121'),"
                          "(0, 'pathogène', 'Cardiovirus D (virus Saffold)', 'Cardiovirus_D', 321, 'virus_122'),"
                          "(0, 'pathogène', 'Cosavirus ', 'Cosavirus', 322, 'virus_123'),"
                          "(0, 'pathogène', 'Cosavirus A', 'Cosavirus_A', 323, 'virus_124'),"
                          "(0, 'pathogène', 'Enterovirus ', 'Enterovirus', 324, 'virus_125'),"
                          "(0, 'pathogène', 'Enterovirus A', 'Enterovirus_A', 325, 'virus_126'),"
                          "(0, 'pathogène', 'Enterovirus B', 'Enterovirus_B', 326, 'virus_127'),"
                          "(0, 'pathogène', 'Enterovirus C', 'Enterovirus_C', 327, 'virus_128'),"
                          "(0, 'pathogène', 'Enterovirus D (entérovirus humain de type 70 [virus de la conjonctivite hémorragique aiguë])', 'Enterovirus_D', 328, 'virus_129'),"
                          "(0, 'pathogène', 'Rhinovirus A, Rhinovirus B et Rhinovirus C', 'Rhinovirus_A,', 329, 'virus_130'),"
                          "(0, 'pathogène', 'Enterovirus C (poliovirus de types 1 et 3)', 'Enterovirus_C_2', 330, 'virus_131'),"
                          "(0, 'pathogène', 'Enterovirus C (poliovirus de type 2)', 'Enterovirus_C_3', 331, 'virus_132'),"
                          "(0, 'pathogène', 'Hepatovirus ', 'Hepatovirus', 332, 'virus_133'),"
                          "(0, 'pathogène', 'Hepatovirus A (virus de l''hépatite A, entérovirus humain de type 72)', 'Hepatovirus_A', 333, 'virus_134'),"
                          "(0, 'pathogène', 'Kobuvirus ', 'Kobuvirus', 334, 'virus_135'),"
                          "(0, 'pathogène', 'Aichivirus A (virus Aichi 1)', 'Aichivirus_A', 335, 'virus_136'),"
                          "(0, 'pathogène', 'Parechovirus ', 'Parechovirus', 336, 'virus_137'),"
                          "(0, 'pathogène', 'Parechovirus A', 'Parechovirus_A', 337, 'virus_138'),"
                          "(0, 'pathogène', 'Parechovirus B (virus Ljungan)', 'Parechovirus_B', 338, 'virus_139'),"
                          "(0, 'pathogène', 'Autres Picornaviridae connus pour être pathogènes', 'Autres_4', 339, 'virus_140'),"
                          "(0, 'pathogène', 'Adenoviridae ', 'Adenoviridae', 340, 'virus_141'),"
                          "(0, 'pathogène', 'Astroviridae ', 'Astroviridae', 341, 'virus_142'),"
                          "(0, 'pathogène', 'Hepadnaviridae ', 'Hepadnaviridae', 342, 'virus_143'),"
                          "(0, 'pathogène', 'Orthohepadnavirus ', 'Orthohepadnavirus', 343, 'virus_144'),"
                          "(0, 'pathogène', 'Hepatitis B virus (virus de l''hépatite B)', 'Hepatitis_B_virus', 344, 'virus_145'),"
                          "(0, 'pathogène', 'Hepelivirales (O)', 'Hepelivirales', 345, 'virus_146'),"
                          "(0, 'pathogène', 'Hepeviridae ', 'Hepeviridae', 346, 'virus_147'),"
                          "(0, 'pathogène', 'Orthohepevirus ', 'Orthohepevirus', 347, 'virus_148'),"
                          "(0, 'pathogène', 'Orthohepevirus A (virus de l''hépatite E)', 'Orthohepevirus_A', 348, 'virus_149'),"
                          "(0, 'pathogène', 'Amarillovirales (O)', 'Amarillovirales', 349, 'virus_150'),"
                          "(0, 'pathogène', 'Flaviviridae ', 'Flaviviridae', 350, 'virus_151'),"
                          "(0, 'pathogène', 'Flavivirus ', 'Flavivirus', 351, 'virus_152'),"
                          "(0, 'pathogène', 'Dengue virus', 'Dengue_virus', 352, 'virus_153'),"
                          "(0, 'pathogène', 'Japanese encephalitis virus', 'Japanese', 353, 'virus_154'),"
                          "(0, 'pathogène', 'Kyasanur Forest disease virus', 'Kyasanur_Forest', 354, 'virus_155'),"
                          "(0, 'pathogène', 'Louping ill virus', 'Louping_ill_virus', 355, 'virus_156'),"
                          "(0, 'pathogène', 'Murray Valley encephalitis virus (virus de l''encéphalite d''Australie)', 'Murray_Valley', 356, 'virus_157'),"
                          "(0, 'pathogène', 'Omsk hemorrhagic fever virus', 'Omsk_hemorrhagic', 357, 'virus_158'),"
                          "(0, 'pathogène', 'Powassan virus', 'Powassan_virus', 358, 'virus_159'),"
                          "(0, 'pathogène', 'Ilheus virus (virus Rocio)', 'Ilheus_virus', 359, 'virus_160'),"
                          "(0, 'pathogène', 'Saint Louis encephalitis virus', 'Saint_Louis', 360, 'virus_161'),"
                          "(0, 'pathogène', 'Tick-borne encephalitis virus(virus de l''encéphalite à tiques)', 'Tick-borne', 361, 'virus_162'),"
                          "(0, 'pathogène', 'Tick-borne encephalitis virus (virus Absettarov, virus Hanzalova, virus Hypr, virus Kumlinge, virus Negishi, et sous type d''Extrême-Orient)', 'Tick-borne_2', 362, 'virus_163'),"
                          "(0, 'pathogène', 'Tick-borne encephalitis virus (virus de l''encéphalite verno-estivale russe, et sous type sibérien)', 'Tick-borne_3', 363, 'virus_164'),"
                          "(0, 'pathogène', 'Tick-borne encephalitis virus (sous type d''Europe centrale)', 'Tick-borne_4', 364, 'virus_165'),"
                          "(0, 'pathogène', 'Wesselsbron virus', 'Wesselsbron_virus', 365, 'virus_166'),"
                          "(0, 'pathogène', 'West Nile virus', 'West_Nile_virus', 366, 'virus_167'),"
                          "(0, 'pathogène', 'Yellow fever virus', 'Yellow_fever_virus', 367, 'virus_168'),"
                          "(0, 'pathogène', 'Zika virus', 'Zika_virus', 368, 'virus_169'),"
                          "(0, 'pathogène', 'Autres flavivirus connus pour être pathogènes', 'Autres_flavivirus', 369, 'virus_170'),"
                          "(0, 'pathogène', 'Hepacivirus ', 'Hepacivirus', 370, 'virus_171'),"
                          "(0, 'pathogène', 'Hepacivirus C (virus de l''hépatite C)', 'Hepacivirus_C', 371, 'virus_172'),"
                          "(0, 'pathogène', 'Orthomyxoviridae ', 'Orthomyxoviridae', 372, 'virus_173'),"
                          "(0, 'pathogène', 'Alphainfluenzavirus ', 'Alphainfluenzavirus', 373, 'virus_174'),"
                          "(0, 'pathogène', 'Influenza A virus', 'Influenza_A_virus', 374, 'virus_175'),"
                          "(0, 'pathogène', 'Influenza A virus (virus hautement pathogènes de l''influenza aviaire HPAIV (H5), par exemple H5N1)', 'Influenza_A_virus_2', 375, 'virus_176'),"
                          "(0, 'pathogène', 'Influenza A virus (virus hautement pathogènes de l''influenza aviaire HPAIV [H7], par exemple H7N7, H7N9)', 'Influenza_A_virus_3', 376, 'virus_177'),"
                          "(0, 'pathogène', 'Influenza A virus (virus influenza de type A/New York/1/18 [H1N1] [grippe espagnole 1918])', 'Influenza_A_virus_4', 377, 'virus_178'),"
                          "(0, 'pathogène', 'Influenza A virus (virus influenza de type A/Singapour/1/57 [H2N2])', 'Influenza_A_virus_5', 378, 'virus_179'),"
                          "(0, 'pathogène', 'Influenza A virus (virus de l''influenza aviaire faiblement pathogène [IAFP] [H7N9])', 'Influenza_A_virus_6', 379, 'virus_180'),"
                          "(0, 'pathogène', 'Betainfluenzavirus ', 'Betainfluenzavirus', 380, 'virus_181'),"
                          "(0, 'pathogène', 'Influenza B virus', 'Influenza_B_virus', 381, 'virus_182'),"
                          "(0, 'pathogène', 'Gammainfluenzavirus ', 'Gammainfluenzavirus', 382, 'virus_183'),"
                          "(0, 'pathogène', 'Influenza C virus', 'Influenza_C_virus', 383, 'virus_184'),"
                          "(0, 'pathogène', 'Thogotovirus ', 'Thogotovirus', 384, 'virus_185'),"
                          "(0, 'pathogène', 'Dhori thogotovirus (orthomyxoviridae à tiques : Dhori)', 'Dhori_thogotovirus', 385, 'virus_186'),"
                          "(0, 'pathogène', 'Thogoto thogotovirus (orthomyxoviridae à tiques : Thogoto)', 'Thogoto_thogotovirus', 386, 'virus_187'),"
                          "(0, 'pathogène', 'Papillomaviridae ', 'Papillomaviridae', 387, 'virus_188'),"
                          "(0, 'pathogène', 'Papillomavirus ', 'Papillomavirus', 388, 'virus_189'),"
                          "(0, 'pathogène', 'Parvoviridae ', 'Parvoviridae', 389, 'virus_190'),"
                          "(0, 'pathogène', 'Erythroparvovirus ', 'Erythroparvovirus', 390, 'virus_191'),"
                          "(0, 'pathogène', 'Primate erythroparvovirus 1 (parvovirus humain, virus B 19)', 'Primate', 391, 'virus_192'),"
                          "(0, 'pathogène', 'Polyomaviridae ', 'Polyomaviridae', 392, 'virus_193'),"
                          "(0, 'pathogène', 'Betapolyomavirus ', 'Betapolyomavirus', 393, 'virus_194'),"
                          "(0, 'pathogène', 'Human polyomavirus 1 (virus BK)', 'Human_polyomavirus_1', 394, 'virus_195'),"
                          "(0, 'pathogène', 'Human polyomavirus 2 (virus JC)', 'Human_polyomavirus_2', 395, 'virus_196'),"
                          "(0, 'pathogène', 'Poxviridae ', 'Poxviridae', 396, 'virus_197'),"
                          "(0, 'pathogène', 'Molluscipoxvirus ', 'Molluscipoxvirus', 397, 'virus_198'),"
                          "(0, 'pathogène', 'Molluscum contagiosum virus', 'Molluscum', 398, 'virus_199'),"
                          "(0, 'pathogène', 'Orthopoxvirus ', 'Orthopoxvirus', 399, 'virus_200'),"
                          "(0, 'pathogène', 'Cowpox virus (virus de la variole bovine)', 'Cowpox_virus', 400, 'virus_201'),"
                          "(0, 'pathogène', 'Monkeypox virus (virus de la variole du singe)', 'Monkeypox_virus', 401, 'virus_202'),"
                          "(0, 'pathogène', 'Vaccinia virus (virus de la vaccine y compris virus de la variole du buffle (d), virus de la variole de l''éléphant (e), virus de la variole du lapin )', 'Vaccinia_virus', 402, 'virus_203'),"
                          "(0, 'pathogène', 'Variola virus (virus de la variole)', 'Variola_virus', 403, 'virus_204'),"
                          "(0, 'pathogène', 'Parapoxvirus ', 'Parapoxvirus', 404, 'virus_205'),"
                          "(0, 'pathogène', 'Orf virus', 'Orf_virus', 405, 'virus_206'),"
                          "(0, 'pathogène', 'Pseudocowpox virus (virus du nodule des trayeurs, parapoxvirus bovis)', 'Pseudocowpox_virus', 406, 'virus_207'),"
                          "(0, 'pathogène', 'Yatapoxvirus ', 'Yatapoxvirus', 407, 'virus_208'),"
                          "(0, 'pathogène', 'Tanapox virus', 'Tanapox_virus', 408, 'virus_209'),"
                          "(0, 'pathogène', 'Yaba monkey tumor virus', 'Yaba_monkey_tumor', 409, 'virus_210'),"
                          "(0, 'pathogène', 'Reoviridae ', 'Reoviridae', 410, 'virus_211'),"
                          "(0, 'pathogène', 'Seadornavirus ', 'Seadornavirus', 411, 'virus_212'),"
                          "(0, 'pathogène', 'Banna virus', 'Banna_virus', 412, 'virus_213'),"
                          "(0, 'pathogène', 'Coltivirus ', 'Coltivirus', 413, 'virus_214'),"
                          "(0, 'pathogène', 'Rotavirus ', 'Rotavirus', 414, 'virus_215'),"
                          "(0, 'pathogène', 'Orbivirus ', 'Orbivirus', 415, 'virus_216'),"
                          "(0, 'pathogène', 'Retroviridae ', 'Retroviridae', 416, 'virus_217'),"
                          "(0, 'pathogène', 'Deltaretrovirus ', 'Deltaretrovirus', 417, 'virus_218'),"
                          "(0, 'pathogène', 'Primate T-lymphotropic virus 1 (virus lymphotrope des cellules T humain de type 1)', 'Primate_2', 418, 'virus_219'),"
                          "(0, 'pathogène', 'Primate T-lymphotropic virus 2 (virus lymphotrope des cellules T humain de type 2)', 'Primate_3', 419, 'virus_220'),"
                          "(0, 'pathogène', 'Lentivirus ', 'Lentivirus', 420, 'virus_221'),"
                          "(0, 'pathogène', 'Human immunodeficiency virus 1 (Virus de l''immunodéficience humaine 1 [VIH-1])', 'Human_13', 421, 'virus_222'),"
                          "(0, 'pathogène', 'Human immunodeficiency virus 2 (Virus de l''immunodéficience humaine 2 [VIH-2])', 'Human_14', 422, 'virus_223'),"
                          "(0, 'pathogène', 'Simian immunodeficiency virus (virus de l''immunodéficience simienne [VIS])', 'Simian', 423, 'virus_224'),"
                          "(0, 'pathogène', 'Togaviridae ', 'Togaviridae', 424, 'virus_225'),"
                          "(0, 'pathogène', 'Alphavirus ', 'Alphavirus', 425, 'virus_226'),"
                          "(0, 'pathogène', 'Cabassou virus', 'Cabassou_virus', 426, 'virus_227'),"
                          "(0, 'pathogène', 'Eastern equine encephalitis virus (virus de l''encéphalomyélite équine est-américaine)', 'Eastern_equine', 427, 'virus_228'),"
                          "(0, 'pathogène', 'Bebaru virus', 'Bebaru_virus', 428, 'virus_229'),"
                          "(0, 'pathogène', 'Chikungunya virus', 'Chikungunya_virus', 429, 'virus_230'),"
                          "(0, 'pathogène', 'Everglades virus', 'Everglades_virus', 430, 'virus_231'),"
                          "(0, 'pathogène', 'Mayaro virus', 'Mayaro_virus', 431, 'virus_232'),"
                          "(0, 'pathogène', 'Mucambo virus', 'Mucambo_virus', 432, 'virus_233'),"
                          "(0, 'pathogène', 'Ndumu virus', 'Ndumu_virus', 433, 'virus_234'),"
                          "(0, 'pathogène', 'Onyong-nyong virus (virus O''nyong-nyong)', 'Onyong-nyong_virus', 434, 'virus_235'),"
                          "(0, 'pathogène', 'Ross River virus', 'Ross_River_virus', 435, 'virus_236'),"
                          "(0, 'pathogène', 'Semliki Forest virus', 'Semliki_Forest_virus', 436, 'virus_237'),"
                          "(0, 'pathogène', 'Sindbis virus', 'Sindbis_virus', 437, 'virus_238'),"
                          "(0, 'pathogène', 'Tonate virus', 'Tonate_virus', 438, 'virus_239'),"
                          "(0, 'pathogène', 'Venezuelan equine encephalitis virus (virus de l''encéphalomyélite équine du Venezuela)', 'Venezuelan_equine', 439, 'virus_240'),"
                          "(0, 'pathogène', 'Western equine encephalitis virus (virus de l''encéphalomyélite équine ouest-américaine)', 'Western_equine', 440, 'virus_241'),"
                          "(0, 'pathogène', 'Autres alphavirus connus pour être pathogènes', 'Autres_alphavirus', 441, 'virus_242'),"
                          "(0, 'pathogène', 'Matonaviridae ', 'Matonaviridae', 442, 'virus_243'),"
                          "(0, 'pathogène', 'Rubivirus ', 'Rubivirus', 443, 'virus_244'),"
                          "(0, 'pathogène', 'Rubivirus rubellae (virus de la rubéole)', 'Rubivirus_rubellae', 444, 'virus_245'),"
                          "(0, 'pathogène', 'Kolmioviridae ', 'Kolmioviridae', 445, 'virus_246'),"
                          "(0, 'pathogène', 'Deltavirus ', 'Deltavirus', 446, 'virus_247'),"
                          "(0, 'pathogène', 'Deltavirus (Virus de l''hépatite delta)', 'Deltavirus_2', 447, 'virus_248')"))
    except Exception as err:
        print("ERROR insert 248 virus pathogen dictionary,\n\terr=" + str(err))

    # insert 91 parasite pathogen dictionary
    try:
        conn.execute(text("INSERT INTO sigl_dico_data (id_owner, dico_name, label, short_label, position, code) VALUES "
                          "(0, 'pathogène', 'Acanthamoeba castellanii', 'Acanthamoeba', 448, 'para_1'),"
                          "(0, 'pathogène', 'Ancylostoma duodenale', 'Ancylostoma', 449, 'para_2'),"
                          "(0, 'pathogène', 'Angiostrongylus cantonensis', 'Angiostrongylus', 450, 'para_3'),"
                          "(0, 'pathogène', 'Angiostrongylus costaricensis', 'Angiostrongylus_2', 451, 'para_4'),"
                          "(0, 'pathogène', 'Anisakis simplex', 'Anisakis_simplex', 452, 'para_5'),"
                          "(0, 'pathogène', 'Ascaris lumbricoides', 'Ascaris_lumbricoides', 453, 'para_6'),"
                          "(0, 'pathogène', 'Ascaris suum', 'Ascaris_suum', 454, 'para_7'),"
                          "(0, 'pathogène', 'Babesia divergens', 'Babesia_divergens', 455, 'para_8'),"
                          "(0, 'pathogène', 'Babesia microti', 'Babesia_microti', 456, 'para_9'),"
                          "(0, 'pathogène', 'Balamuthia mandrillaris', 'Balamuthia', 457, 'para_10'),"
                          "(0, 'pathogène', 'Balantidium coli', 'Balantidium_coli', 458, 'para_11'),"
                          "(0, 'pathogène', 'Brugia malayi', 'Brugia_malayi', 459, 'para_12'),"
                          "(0, 'pathogène', 'Brugia pahangi', 'Brugia_pahangi', 460, 'para_13'),"
                          "(0, 'pathogène', 'Brugia timori', 'Brugia_timori', 461, 'para_14'),"
                          "(0, 'pathogène', 'Capillaria philippinensis', 'Capillaria', 462, 'para_15'),"
                          "(0, 'pathogène', 'Capillaria spp.', 'Capillaria_spp.', 463, 'para_16'),"
                          "(0, 'pathogène', 'Clonorchis sinensis (Opisthorchis sinensis)', 'Clonorchis_sinensis', 464, 'para_17'),"
                          "(0, 'pathogène', 'Clonorchis viverrini (Opisthirchis viverrini)', 'Clonorchis_viverrini', 465, 'para_18'),"
                          "(0, 'pathogène', 'Cryptosporidium hominis', 'Cryptosporidium', 466, 'para_19'),"
                          "(0, 'pathogène', 'Cryptosporidium parvum', 'Cryptosporidium_2', 467, 'para_20'),"
                          "(0, 'pathogène', 'Cyclospora cayetanensis', 'Cyclospora', 468, 'para_21'),"
                          "(0, 'pathogène', 'Dicrocoelium dentriticum', 'Dicrocoelium', 469, 'para_22'),"
                          "(0, 'pathogène', 'Dipetalonema streptocerca', 'Dipetalonema', 470, 'para_23'),"
                          "(0, 'pathogène', 'Diphyllobothrium latum', 'Diphyllobothrium', 471, 'para_24'),"
                          "(0, 'pathogène', 'Dracunculus medinensis', 'Dracunculus', 472, 'para_25'),"
                          "(0, 'pathogène', 'Echinococcus granulosus', 'Echinococcus', 473, 'para_26'),"
                          "(0, 'pathogène', 'Echinococcus multilocularis', 'Echinococcus_2', 474, 'para_27'),"
                          "(0, 'pathogène', 'Echinococcus oligarthrus', 'Echinococcus_3', 475, 'para_28'),"
                          "(0, 'pathogène', 'Echinococcus vogeli', 'Echinococcus_vogeli', 476, 'para_29'),"
                          "(0, 'pathogène', 'Entamoeba histolytica', 'Entamoeba', 477, 'para_30'),"
                          "(0, 'pathogène', 'Enterobius vermicularis', 'Enterobius', 478, 'para_31'),"
                          "(0, 'pathogène', 'Enterocytozoon bieneusi', 'Enterocytozoon', 479, 'para_32'),"
                          "(0, 'pathogène', 'Fasciola gigantica', 'Fasciola_gigantica', 480, 'para_33'),"
                          "(0, 'pathogène', 'Fasciola hepatica', 'Fasciola_hepatica', 481, 'para_34'),"
                          "(0, 'pathogène', 'Fasciolopsis buski', 'Fasciolopsis_buski', 482, 'para_35'),"
                          "(0, 'pathogène', 'Giardia lamblia (Giardia duodenalis, Giardia intestinalis)', 'Giardia_lamblia', 483, 'para_36'),"
                          "(0, 'pathogène', 'Heterophyes spp.', 'Heterophyes_spp.', 484, 'para_37'),"
                          "(0, 'pathogène', 'Hymenolepis diminuta', 'Hymenolepis_diminuta', 485, 'para_38'),"
                          "(0, 'pathogène', 'Hymenolepis nana', 'Hymenolepis_nana', 486, 'para_39'),"
                          "(0, 'pathogène', 'Leishmania aethiopica', 'Leishmania', 487, 'para_40'),"
                          "(0, 'pathogène', 'Leishmania braziliensis', 'Leishmania_2', 488, 'para_41'),"
                          "(0, 'pathogène', 'Leishmania donovani', 'Leishmania_donovani', 489, 'para_42'),"
                          "(0, 'pathogène', 'Leishmania guyanensis (Viannia guyanensis)', 'Leishmania_3', 490, 'para_43'),"
                          "(0, 'pathogène', 'Leishmania infantum (Leishmania chagasi)', 'Leishmania_infantum', 491, 'para_44'),"
                          "(0, 'pathogène', 'Leishmania major', 'Leishmania_major', 492, 'para_45'),"
                          "(0, 'pathogène', 'Leishmania mexicana', 'Leishmania_mexicana', 493, 'para_46'),"
                          "(0, 'pathogène', 'Leishmania panamensis (Viannia panamensis)', 'Leishmania_4', 494, 'para_47'),"
                          "(0, 'pathogène', 'Leishmania peruviana', 'Leishmania_peruviana', 495, 'para_48'),"
                          "(0, 'pathogène', 'Leishmania tropica', 'Leishmania_tropica', 496, 'para_49'),"
                          "(0, 'pathogène', 'Leishmania spp.', 'Leishmania_spp.', 497, 'para_50'),"
                          "(0, 'pathogène', 'Loa loa', 'Loa_loa', 498, 'para_51'),"
                          "(0, 'pathogène', 'Mansonella ozzardi', 'Mansonella_ozzardi', 499, 'para_52'),"
                          "(0, 'pathogène', 'Mansonella perstans', 'Mansonella_perstans', 500, 'para_53'),"
                          "(0, 'pathogène', 'Mansonella streptocerca', 'Mansonella', 501, 'para_54'),"
                          "(0, 'pathogène', 'Metagonimus spp.', 'Metagonimus_spp.', 502, 'para_55'),"
                          "(0, 'pathogène', 'Naegleria fowleri', 'Naegleria_fowleri', 503, 'para_56'),"
                          "(0, 'pathogène', 'Necator americanus', 'Necator_americanus', 504, 'para_57'),"
                          "(0, 'pathogène', 'Onchocerca volvulus', 'Onchocerca_volvulus', 505, 'para_58'),"
                          "(0, 'pathogène', 'Opisthorchis felineus', 'Opisthorchis', 506, 'para_59'),"
                          "(0, 'pathogène', 'Opisthorchis spp.', 'Opisthorchis_spp.', 507, 'para_60'),"
                          "(0, 'pathogène', 'Paragonimus westermani', 'Paragonimus', 508, 'para_61'),"
                          "(0, 'pathogène', 'Paragonimus spp.', 'Paragonimus_spp.', 509, 'para_62'),"
                          "(0, 'pathogène', 'Plasmodium falciparum', 'Plasmodium', 510, 'para_63'),"
                          "(0, 'pathogène', 'Plasmodium knowlesi', 'Plasmodium_knowlesi', 511, 'para_64'),"
                          "(0, 'pathogène', 'Plasmodium spp. (humain et simien)', 'Plasmodium_spp.', 512, 'para_65'),"
                          "(0, 'pathogène', 'Sarcocystis suihominis', 'Sarcocystis', 513, 'para_66'),"
                          "(0, 'pathogène', 'Schistosoma haematobium', 'Schistosoma', 514, 'para_67'),"
                          "(0, 'pathogène', 'Schistosoma intercalatum', 'Schistosoma_2', 515, 'para_68'),"
                          "(0, 'pathogène', 'Schistosoma japonicum', 'Schistosoma_3', 516, 'para_69'),"
                          "(0, 'pathogène', 'Schistosoma mansoni', 'Schistosoma_mansoni', 517, 'para_70'),"
                          "(0, 'pathogène', 'Schistosoma mekongi', 'Schistosoma_mekongi', 518, 'para_71'),"
                          "(0, 'pathogène', 'Strongyloides stercoralis', 'Strongyloides', 519, 'para_72'),"
                          "(0, 'pathogène', 'Strongyloides spp.', 'Strongyloides_spp.', 520, 'para_73'),"
                          "(0, 'pathogène', 'Taenia saginata', 'Taenia_saginata', 521, 'para_74'),"
                          "(0, 'pathogène', 'Taenia solium', 'Taenia_solium', 522, 'para_75'),"
                          "(0, 'pathogène', 'Toxocara canis', 'Toxocara_canis', 523, 'para_76'),"
                          "(0, 'pathogène', 'Toxocara cati', 'Toxocara_cati', 524, 'para_77'),"
                          "(0, 'pathogène', 'Toxoplasma gondii', 'Toxoplasma_gondii', 525, 'para_78'),"
                          "(0, 'pathogène', 'Trichinella nativa', 'Trichinella_nativa', 526, 'para_79'),"
                          "(0, 'pathogène', 'Trichinella nelsoni', 'Trichinella_nelsoni', 527, 'para_80'),"
                          "(0, 'pathogène', 'Trichinella pseudospiralis', 'Trichinella', 528, 'para_81'),"
                          "(0, 'pathogène', 'Trichinella spiralis', 'Trichinella_spiralis', 529, 'para_82'),"
                          "(0, 'pathogène', 'Trichomonas vaginalis', 'Trichomonas', 530, 'para_83'),"
                          "(0, 'pathogène', 'Trichostrongylus orientalis', 'Trichostrongylus', 531, 'para_84'),"
                          "(0, 'pathogène', 'Trichostrongylus spp.', 'Trichostrongylus_2', 532, 'para_85'),"
                          "(0, 'pathogène', 'Trichuris trichiura', 'Trichuris_trichiura', 533, 'para_86'),"
                          "(0, 'pathogène', 'Trypanosoma brucei brucei', 'Trypanosoma_brucei', 534, 'para_87'),"
                          "(0, 'pathogène', 'Trypanosoma brucei gambiense', 'Trypanosoma_brucei_2', 535, 'para_88'),"
                          "(0, 'pathogène', 'Trypanosoma brucei rhodesiense', 'Trypanosoma_brucei_3', 536, 'para_89'),"
                          "(0, 'pathogène', 'Trypanosoma cruzi', 'Trypanosoma_cruzi', 537, 'para_90'),"
                          "(0, 'pathogène', 'Wuchereria bancrofti', 'Wuchereria_bancrofti', 538, 'para_91')"))
    except Exception as err:
        print("ERROR insert 91 parasite pathogen dictionary,\n\terr=" + str(err))

    # insert 41 fungi pathogen dictionary
    try:
        conn.execute(text("INSERT INTO sigl_dico_data (id_owner, dico_name, label, short_label, position, code) VALUES "
                          "(0, 'pathogène', 'Aspergillus flavus', 'Aspergillus_flavus', 539, 'fungi_1'),"
                          "(0, 'pathogène', 'Aspergillus fumigatus', 'Aspergillus', 540, 'fungi_2'),"
                          "(0, 'pathogène', 'Aspergillus spp.', 'Aspergillus_spp.', 541, 'fungi_3'),"
                          "(0, 'pathogène', 'Blastomyces dermatitidis (Ajellomyces dermatitidis)', 'Blastomyces', 542, 'fungi_4'),"
                          "(0, 'pathogène', 'Blastomyces gilchristii', 'Blastomyces_2', 543, 'fungi_5'),"
                          "(0, 'pathogène', 'Candida albicans', 'Candida_albicans', 544, 'fungi_6'),"
                          "(0, 'pathogène', 'Candida dubliniensis', 'Candida_dubliniensis', 545, 'fungi_7'),"
                          "(0, 'pathogène', 'Candida glabrata', 'Candida_glabrata', 546, 'fungi_8'),"
                          "(0, 'pathogène', 'Candida parapsilosis', 'Candida_parapsilosis', 547, 'fungi_9'),"
                          "(0, 'pathogène', 'Candida tropicalis', 'Candida_tropicalis', 548, 'fungi_10'),"
                          "(0, 'pathogène', 'Cladophialophora bantiana', 'Cladophialophora', 549, 'fungi_11'),"
                          "(0, 'pathogène', 'Cladophialophora modesta', 'Cladophialophora_2', 550, 'fungi_12'),"
                          "(0, 'pathogène', 'Cladophialophora spp.', 'Cladophialophora_3', 551, 'fungi_13'),"
                          "(0, 'pathogène', 'Coccidioides immitis', 'Coccidioides_immitis', 552, 'fungi_14'),"
                          "(0, 'pathogène', 'Coccidioides posadasii', 'Coccidioides', 553, 'fungi_15'),"
                          "(0, 'pathogène', 'Cryptococcus gattii', 'Cryptococcus_gattii', 554, 'fungi_16'),"
                          "(0, 'pathogène', 'Cryptococcus neoformans', 'Cryptococcus', 555, 'fungi_17'),"
                          "(0, 'pathogène', 'Emmonsia parva var. parva', 'Emmonsia_parva_var.', 556, 'fungi_18'),"
                          "(0, 'pathogène', 'Emmonsia parva var. crescens', 'Emmonsia_parva_var._2', 557, 'fungi_19'),"
                          "(0, 'pathogène', 'Epidermophyton floccosum', 'Epidermophyton', 558, 'fungi_20'),"
                          "(0, 'pathogène', 'Epidermophyton spp.', 'Epidermophyton_spp.', 559, 'fungi_21'),"
                          "(0, 'pathogène', 'Fonsecaea pedrosoi', 'Fonsecaea_pedrosoi', 560, 'fungi_22'),"
                          "(0, 'pathogène', 'Histoplasma capsulatum', 'Histoplasma', 561, 'fungi_23'),"
                          "(0, 'pathogène', 'Histoplasma capsulatum var. farciminosum', 'Histoplasma_2', 562, 'fungi_24'),"
                          "(0, 'pathogène', 'Histoplasma capsulatum var. duboisii', 'Histoplasma_3', 563, 'fungi_25'),"
                          "(0, 'pathogène', 'Madurella grisea', 'Madurella_grisea', 564, 'fungi_26'),"
                          "(0, 'pathogène', 'Madurella mycetomatis', 'Madurella', 565, 'fungi_27'),"
                          "(0, 'pathogène', 'Microsporum spp.', 'Microsporum_spp.', 566, 'fungi_28'),"
                          "(0, 'pathogène', 'Nannizzia spp.', 'Nannizzia_spp.', 567, 'fungi_29'),"
                          "(0, 'pathogène', 'Neotestudina rosatii', 'Neotestudina_rosatii', 568, 'fungi_30'),"
                          "(0, 'pathogène', 'Paracoccidioides brasiliensis', 'Paracoccidioides', 569, 'fungi_31'),"
                          "(0, 'pathogène', 'Paracoccidioides lutzii', 'Paracoccidioides_2', 570, 'fungi_32'),"
                          "(0, 'pathogène', 'Paraphyton spp.', 'Paraphyton_spp.', 571, 'fungi_33'),"
                          "(0, 'pathogène', 'Rhinocladiella mackenziei', 'Rhinocladiella', 572, 'fungi_34'),"
                          "(0, 'pathogène', 'Scedosporium apiospermum', 'Scedosporium', 573, 'fungi_35'),"
                          "(0, 'pathogène', 'Scedosporium prolificans (inflatum)', 'Scedosporium_2', 574, 'fungi_36'),"
                          "(0, 'pathogène', 'Sporothrix schenckii', 'Sporothrix_schenckii', 575, 'fungi_37'),"
                          "(0, 'pathogène', 'Talaromyces marneffei (Penicillium marneffei)', 'Talaromyces', 576, 'fungi_38'),"
                          "(0, 'pathogène', 'Trichophyton rubrum', 'Trichophyton_rubrum', 577, 'fungi_39'),"
                          "(0, 'pathogène', 'Trichophyton tonsurans', 'Trichophyton', 578, 'fungi_40'),"
                          "(0, 'pathogène', 'Trichophyton spp.', 'Trichophyton_spp.', 579, 'fungi_41')"))
    except Exception as err:
        print("ERROR insert 41 fungus pathogen dictionary,\n\terr=" + str(err))

    # Insert profile rights
    try:
        conn.execute(text('''
                          insert into profile_rights (prr_ser, prr_date, prr_by_user, prr_rank, prr_type, prr_label, prr_tag)
                          values
                          (169, NOW(), 0, 28000,"ALIQUOT","Gestion des échantillons", "ALIQUOT_169"),
                          (170, NOW(), 0, 28020,"ALIQUOT","Ajouter un élement", "ALIQUOT_170"),
                          (171, NOW(), 0, 28040,"ALIQUOT","Editer un élement", "ALIQUOT_171"),
                          (172, NOW(), 0, 28050,"ALIQUOT","Déstocker un élement", "ALIQUOT_172"),
                          (173, NOW(), 0, 28060,"ALIQUOT","Supprimer un élément", "ALIQUOT_173")
                          '''))
    except Exception as err:
        print("ERROR insert default profile_rights,\n\terr=" + str(err))

    # Insert default permissions for Admin (pro_ser = 1)
    try:
        conn.execute(text('''
            INSERT INTO profile_permissions (prp_date, prp_by_user, prp_pro, prp_prr, prp_granted)
            SELECT NOW(), 0, 1, prr_ser, 'Y'
            FROM profile_rights
            WHERE prr_ser BETWEEN 169 AND 173
        '''))
    except Exception as err:
        print("ERROR inserting default profile_permissions Admin,\n\terr=" + str(err))

    # Insert default permissions for Biologist (pro_ser = 3)
    try:
        conn.execute(text('''
            INSERT INTO profile_permissions (prp_date, prp_by_user, prp_pro, prp_prr, prp_granted)
            SELECT NOW(), 0, 3, prr_ser, 'Y'
            FROM profile_rights
            WHERE prr_ser BETWEEN 169 AND 173
        '''))
    except Exception as err:
        print("ERROR inserting default profile_permissions Biologist,\n\terr=" + str(err))

    # Insert default permissions for Technician Advanced (pro_ser = 11)
    try:
        conn.execute(text('''
            INSERT INTO profile_permissions (prp_date, prp_by_user, prp_pro, prp_prr, prp_granted)
            SELECT NOW(), 0, 11, prr_ser, 'Y'
            FROM profile_rights
            WHERE prr_ser BETWEEN 169 AND 173
        '''))
    except Exception as err:
        print("ERROR inserting default profile_permissions Technician Advanced,\n\terr=" + str(err))

    # Insert default permissions for Others (pro_ser not in 1, 3, 11)
    try:
        conn.execute(text('''
            INSERT INTO profile_permissions (prp_date, prp_by_user, prp_pro, prp_prr, prp_granted)
            SELECT NOW(), 0, prp_pro, prr_ser, 'Y'
            FROM profile_rights
            CROSS JOIN (
                SELECT prp_pro FROM profile_permissions
                WHERE prp_pro NOT IN (1, 3, 11)
                GROUP BY prp_pro
            ) AS valid_profiles
            WHERE prr_ser BETWEEN 169 AND 173
        '''))
    except Exception as err:
        print("ERROR inserting profile_permissions others,\n\terr=" + str(err))

    # ADD COLUMN ana_loinc
    try:
        conn.execute(text("alter table sigl_05_data add column ana_loinc varchar(20) default ''"))
    except Exception as err:
        print("ERROR add column ana_loinc to sigl_05_data,\n\terr=" + str(err))

    # ADD COLUMN ana_loinc in table test
    try:
        conn.execute(text("alter table sigl_05_data_test add column ana_loinc varchar(20) default ''"))
    except Exception as err:
        print("ERROR add column ana_loinc to sigl_05_data_test,\n\terr=" + str(err))

    # UPDATE ana_loinc
    try:
        conn.execute(text('''
                          UPDATE sigl_05_data
                          SET ana_loinc = CASE
                              WHEN code = 'B052' THEN '1690-7'
                              WHEN code = 'B001' THEN '14933-6'
                              WHEN code = 'B030' THEN '1751-7'
                              WHEN code = 'B031' THEN '1751-7'
                              WHEN code = 'B270' THEN '5643-2'
                              WHEN code = 'B272' THEN '14593-8'
                              WHEN code = 'B007' THEN '16362-6'
                              WHEN code = 'B049' THEN '1798-8'
                              WHEN code = 'B601' THEN '29576-6'
                              WHEN code = 'B165' THEN '58713-9'
                              WHEN code = 'B287' THEN '16403-8'
                              WHEN code = 'B182' THEN '44357-2'
                              WHEN code = 'B752' THEN '24357-6'
                              WHEN code = 'B275' THEN '19270-8'
                              WHEN code = 'B274' THEN '19270-8'
                              WHEN code = 'B062' THEN '21198-7'
                              WHEN code = 'B002' THEN '1963-8'
                              WHEN code = 'B503' THEN '24331-1'
                              WHEN code = 'B003' THEN '75697-3'
                              WHEN code = 'B167' THEN '98205-8'
                              WHEN code = 'B168' THEN '19053-8'
                              WHEN code = 'B183' THEN '56156-3'
                              WHEN code = 'B169' THEN '100120-5'
                              WHEN code = 'B170' THEN '80363-5'
                              WHEN code = 'B617' THEN '88847-9'
                              WHEN code = 'B022' THEN '24331-1'
                              WHEN code = 'B023' THEN '22748-8'
                              WHEN code = 'B021' THEN '14647-2'
                              WHEN code = 'B024' THEN '24331-1'
                              WHEN code = 'B107' THEN '54231-6'
                              WHEN code = 'B116' THEN '34555-3'
                              WHEN code = 'B063' THEN '14675-3'
                              WHEN code = 'B050' THEN '2157-6'
                              WHEN code = 'B051' THEN '32673-3'
                              WHEN code = 'B004' THEN '45066-8'
                              WHEN code = 'B084' THEN '14637-3'
                              WHEN code = 'B184' THEN '100128-8'
                              WHEN code = 'B248' THEN '58433-4'
                              WHEN code = 'B147' THEN '55398-2'
                              WHEN code = 'B185' THEN '25389-8'
                              WHEN code = 'B187' THEN '100105-6'
                              WHEN code = 'B189' THEN '5238-1'
                              WHEN code = 'B781' THEN '98212-4'
                              WHEN code = 'B798' THEN '75317-2'
                              WHEN code = 'B797' THEN '7855-0'
                              WHEN code = 'B504' THEN '88746-3'
                              WHEN code = 'B157' THEN '93923-1'
                              WHEN code = 'B213' THEN '97860-1'
                              WHEN code = 'B800' THEN '97872-6'
                              WHEN code = 'B278' THEN '10535-3'
                              WHEN code = 'B150' THEN '55398-2'
                              WHEN code = 'B222' THEN '19113-0'
                              WHEN code = 'B148' THEN '3255-7'
                              WHEN code = 'B033' THEN '43113-0'
                              WHEN code = 'B025' THEN '24351-9'
                              WHEN code = 'B109' THEN '24352-7'
                              WHEN code = 'B098' THEN '34539-7'
                              WHEN code = 'B064' THEN '15061-5'
                              WHEN code = 'B065' THEN '14715-7'
                              WHEN code = 'B788' THEN '88837-0'
                              WHEN code = 'B789' THEN '88844-6'
                              WHEN code = 'B790' THEN '88845-3'
                              WHEN code = 'B787' THEN '88839-6'
                              WHEN code = 'B778' THEN '88836-2'
                              WHEN code = 'B779' THEN '88864-4'
                              WHEN code = 'B786' THEN '88839-6'
                              WHEN code = 'B782' THEN '88837-0'
                              WHEN code = 'B259' THEN '88841-2'
                              WHEN code = 'B258' THEN '88847-9'
                              WHEN code = 'B249' THEN '88848-7'
                              WHEN code = 'B256' THEN '88841-2'
                              WHEN code = 'B253' THEN '88840-4'
                              WHEN code = 'B251' THEN '88849-5'
                              WHEN code = 'B254' THEN '88838-8'
                              WHEN code = 'B261' THEN '88847-9'
                              WHEN code = 'B255' THEN '88848-7'
                              WHEN code = 'B164' THEN '46437-0'
                              WHEN code = 'B756' THEN '46437-0'
                              WHEN code = 'B010' THEN '50190-8'
                              WHEN code = 'B066' THEN '2276-4'
                              WHEN code = 'B608' THEN '97868-4'
                              WHEN code = 'B616' THEN '40745-2'
                              WHEN code = 'B785' THEN '57022-6'
                              WHEN code = 'B067' THEN '15067-2'
                              WHEN code = 'B053' THEN '2324-2'
                              WHEN code = 'B048' THEN '24338-6'
                              WHEN code = 'B005' THEN '14749-6'
                              WHEN code = 'B750' THEN '81324-6'
                              WHEN code = 'B172' THEN '100113-0'
                              WHEN code = 'B128' THEN '11153-4'
                              WHEN code = 'B257' THEN '88850-3'
                              WHEN code = 'B037' THEN '4576-5'
                              WHEN code = 'B036' THEN '4548-4'
                              WHEN code = 'B038' THEN '6864-3'
                              WHEN code = 'B757' THEN '57022-6'
                              WHEN code = 'B151' THEN '3270-6'
                              WHEN code = 'B203' THEN '95147-5'
                              WHEN code = 'B204' THEN '95206-9'
                              WHEN code = 'B209' THEN '50023-1'
                              WHEN code = 'B216' THEN '90229-6'
                              WHEN code = 'B118' THEN '81324-6'
                              WHEN code = 'B068' THEN '14796-7'
                              WHEN code = 'B069' THEN '14796-7'
                              WHEN code = 'B013' THEN '24326-1'
                              WHEN code = 'B011' THEN '24326-1'
                              WHEN code = 'B055' THEN '14804-9'
                              WHEN code = 'B070' THEN '10501-5'
                              WHEN code = 'B061' THEN '3040-3'
                              WHEN code = 'B026' THEN '1869-7'
                              WHEN code = 'B027' THEN '1884-6'
                              WHEN code = 'B028' THEN '1869-7'
                              WHEN code = 'B014' THEN '14334-7'
                              WHEN code = 'B016' THEN '2597-3'
                              WHEN code = 'B015' THEN '2601-3'
                              WHEN code = 'B130' THEN '30341-2'
                              WHEN code = 'B099' THEN '58447-4'
                              WHEN code = 'B174' THEN '58733-7'
                              WHEN code = 'B039' THEN '2639-3'
                              WHEN code = 'B571' THEN '47385-0'
                              WHEN code = 'B135' THEN '57022-6'
                              WHEN code = 'B137' THEN '57022-6'
                              WHEN code = 'B136' THEN '65759-3'
                              WHEN code = 'B139' THEN '53800-9'
                              WHEN code = 'B138' THEN '50262-5'
                              WHEN code = 'B574' THEN '3877-8'
                              WHEN code = 'B576' THEN '3882-8'
                              WHEN code = 'B191' THEN '70569-9'
                              WHEN code = 'B282' THEN '3298-7'
                              WHEN code = 'B056' THEN '6768-6'
                              WHEN code = 'B017' THEN '14879-1'
                              WHEN code = 'B283' THEN '17052-2'
                              WHEN code = 'B018' THEN '24329-5'
                              WHEN code = 'B019' THEN '2823-3'
                              WHEN code = 'PB24' THEN '88849-5'
                              WHEN code = 'PB25' THEN '88839-6'
                              WHEN code = 'B071' THEN '14890-8'
                              WHEN code = 'B072' THEN '2842-3'
                              WHEN code = 'B044' THEN '1988-5'
                              WHEN code = 'B097' THEN '2885-2'
                              WHEN code = 'B040' THEN '95801-7'
                              WHEN code = 'B041' THEN '95801-7'
                              WHEN code = 'B777' THEN '2885-2'
                              WHEN code = 'B042' THEN '2885-2'
                              WHEN code = 'B112' THEN '2464-6'
                              WHEN code = 'B100' THEN '2889-4'
                              WHEN code = 'B200' THEN '95149-1'
                              WHEN code = 'B201' THEN '95146-7'
                              WHEN code = 'B273' THEN '80148-0'
                              WHEN code = 'B242' THEN '40745-2'
                              WHEN code = 'B238' THEN '32819-5'
                              WHEN code = 'B144' THEN '88836-2'
                              WHEN code = 'b783' THEN '57022-6'
                              WHEN code = 'B205' THEN '95206-9'
                              WHEN code = 'B799' THEN '41878-0'
                              WHEN code = 'B262' THEN '88847-9'
                              WHEN code = 'B233' THEN '1952-1'
                              WHEN code = 'B212' THEN '53601-1'
                              WHEN code = 'B232' THEN '53764-7'
                              WHEN code = 'B231' THEN '2857-1'
                              WHEN code = 'B5271b' THEN '94531-1'
                              WHEN code = 'B609' THEN '90253-6'
                              WHEN code = 'B176' THEN '98212-4'
                              WHEN code = 'B220' THEN '34952-2'
                              WHEN code = 'B175' THEN '98211-6'
                              WHEN code = 'B615' THEN '10704-5'
                              WHEN code = 'B096' THEN '24326-1'
                              WHEN code = 'B578' THEN '3906-5'
                              WHEN code = 'B579' THEN '3911-5'
                              WHEN code = 'B158' THEN '93951-2'
                              WHEN code = 'B094' THEN '13539-2'
                              WHEN code = 'B057' THEN '6768-6'
                              WHEN code = 'B580' THEN '3972-7'
                              WHEN code = 'B095' THEN '2828-2'
                              WHEN code = 'B700' THEN '2823-3'
                              WHEN code = 'B045' THEN '1988-5'
                              WHEN code = 'B043' THEN '1988-5'
                              WHEN code = 'B607' THEN '11001-5'
                              WHEN code = 'B284' THEN '6694-4'
                              WHEN code = 'B197' THEN '95149-1'
                              WHEN code = 'B198' THEN '95149-1'
                              WHEN code = 'B195' THEN '95149-1'
                              WHEN code = 'B199' THEN '95148-3'
                              WHEN code = 'B196' THEN '95148-3'
                              WHEN code = 'B505' THEN '95148-3'
                              WHEN code = 'B194' THEN '95148-3'
                              WHEN code = 'B140' THEN '57022-6'
                              WHEN code = 'B784' THEN '57022-6'
                              WHEN code = 'B243' THEN '88842-0'
                              WHEN code = 'B145' THEN '88836-2'
                              WHEN code = 'B211' THEN '95206-9'
                              WHEN code = 'B210' THEN '95206-9'
                              WHEN code = 'B230' THEN '2039-6'
                              WHEN code = 'B285' THEN '4021-2'
                              WHEN code = 'B218' THEN '88847-9'
                              WHEN code = 'B154' THEN '50197-3'
                              WHEN code = 'B152' THEN '34528-0'
                              WHEN code = 'B006' THEN '22664-7'
                              WHEN code = 'B091' THEN '22700-9'
                              WHEN code = 'B269' THEN '4024-6'
                              WHEN code = 'B082' THEN '14934-4'
                              WHEN code = 'B093' THEN '2078-4'
                              WHEN code = 'B541' THEN '80608-3'
                              WHEN code = 'B525' THEN '3443-9'
                              WHEN code = 'B527' THEN '16567-0'
                              WHEN code = 'B591' THEN '34378-0'
                              WHEN code = 'B502' THEN '75697-3'
                              WHEN code = 'B501' THEN '75697-3'
                              WHEN code = 'B264' THEN '54231-6'
                              WHEN code = 'B008' THEN '2000-8'
                              WHEN code = 'B544' THEN '3484-3'
                              WHEN code = 'B545' THEN '3486-8'
                              WHEN code = 'B546' THEN '16645-4'
                              WHEN code = 'B584' THEN '4021-2'
                              WHEN code = 'B5271a' THEN '94503-0'
                              WHEN code = 'B229' THEN '59564-5'
                              WHEN code = 'B146' THEN '55398-2'
                              WHEN code = 'B181' THEN '44038-8'
                              WHEN code = 'B034' THEN '43113-0'
                              WHEN code = 'B032' THEN '43113-0'
                              WHEN code = 'B035' THEN '24351-9'
                              WHEN code = 'B802' THEN '97872-6'
                              WHEN code = 'B119' THEN '59179-2'
                              WHEN code = 'B801' THEN '97872-6'
                              WHEN code = 'B179' THEN '98212-4'
                              WHEN code = 'B780' THEN '88836-2'
                              WHEN code = 'B602' THEN '88837-0'
                              WHEN code = 'B245' THEN '34383-0'
                              WHEN code = 'B235' THEN '10704-5'
                              WHEN code = 'B556' THEN '35668-3'
                              WHEN code = 'B244' THEN '5238-1'
                              WHEN code = 'B090' THEN '53094-9'
                              WHEN code = 'B751' THEN '14744-7'
                              WHEN code = 'B160' THEN '79160-8'
                              WHEN code = 'B758' THEN '57022-6'
                              WHEN code = 'B759' THEN '57022-6'
                              WHEN code = 'B760' THEN '57022-6'
                              WHEN code = 'B761' THEN '57022-6'
                              WHEN code = 'B762' THEN '57022-6'
                              WHEN code = 'B763' THEN '57022-6'
                              WHEN code = 'B764' THEN '57022-6'
                              WHEN code = 'B765' THEN '57022-6'
                              WHEN code = 'B766' THEN '57022-6'
                              WHEN code = 'B767' THEN '57022-6'
                              WHEN code = 'B768' THEN '57022-6'
                              WHEN code = 'B134' THEN '57022-6'
                              WHEN code = 'B581' THEN '3972-7'
                              WHEN code = 'B559' THEN '47395-9'
                              WHEN code = 'B279' THEN '3697-0'
                              WHEN code = 'B557' THEN '17010-0'
                              WHEN code = 'B606' THEN '3607-9'
                              WHEN code = 'B512' THEN '3344-9'
                              WHEN code = 'B513' THEN '16365-9'
                              WHEN code = 'B511' THEN '35669-1'
                              WHEN code = 'B186' THEN '100088-4'
                              WHEN code = 'B208' THEN '75887-0'
                              WHEN code = 'B4721' THEN '94503-0'
                              WHEN code = 'B104' THEN '19080-1'
                              WHEN code = 'B075' THEN '14913-8'
                              WHEN code = 'B286' THEN '4049-3'
                              WHEN code = 'B073' THEN '3013-0'
                              WHEN code = 'B594' THEN '4054-3'
                              WHEN code = 'B595' THEN '4055-0'
                              WHEN code = 'B597' THEN '35670-9'
                              WHEN code = 'B611' THEN '88746-3'
                              WHEN code = 'B177' THEN '98212-4'
                              WHEN code = 'B077' THEN '3034-6'
                              WHEN code = 'B029' THEN '14927-8'
                              WHEN code = 'B598' THEN '18258-4'
                              WHEN code = 'B080' THEN '3016-3'
                              WHEN code = 'B006' THEN '22664-7'
                              WHEN code = 'B600' THEN '20578-1'
                              WHEN code = 'B221' THEN '72885-7'
                              ELSE ana_loinc
                          END
                          '''))
    except Exception as err:
        print("ERROR update sigl_05_data set ana_loinc,\n\terr=" + str(err))

    # rename table analyzer_lab28 to analyzer_msg
    try:
        conn.execute(text("alter table analyzer_lab28 rename to analyzer_msg"))
    except Exception as err:
        print("ERROR rename analyzer_lab28 to analyzer_msg,\n\terr=" + str(err))

    # rename column from analyzer_lab28
    try:
        conn.execute(text('''
                          alter table analyzer_msg
                          RENAME COLUMN anl_ser TO anm_ser,
                          RENAME COLUMN anl_date TO anm_date,
                          RENAME COLUMN anl_date_upd TO anm_date_upd,
                          RENAME COLUMN anl_id_samp TO anm_id_samp,
                          RENAME COLUMN anl_stat TO anm_stat,
                          RENAME COLUMN anl_OML_O33 TO anm_msg_sent,
                          RENAME COLUMN anl_ORL_O34 TO anm_msg_recv,
                          RENAME COLUMN anl_ans TO anm_ans
                          '''))
    except Exception as err:
        print("ERROR rename column from analyzer_lab28,\n\terr=" + str(err))

    # ADD COLUMN for anm_tot in analyzer_msg for type of transaction
    try:
        conn.execute(text("ALTER TABLE analyzer_msg ADD COLUMN anm_tot VARCHAR(20) NOT NULL DEFAULT ''"))
    except Exception as err:
        print("ERROR add column anm_tot to analyzer_msg,\n\terr=" + str(err))

    # ADD index on anm_tot
    try:
        conn.execute(text("CREATE INDEX idx_anm_tot ON analyzer_msg(anm_tot)"))
    except Exception as err:
        print("ERROR add index anm_tot to analyzer_msg,\n\terr=" + str(err))

    print(str(datetime.today()) + " : END of migration V3_5_3_user_signature revision=14d207abf78f")


def downgrade():
    pass
