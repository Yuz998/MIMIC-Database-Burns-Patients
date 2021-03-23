# %%
import csv
import os
import numpy as np
import pandas as pd
import pymysql
from pymysql import connect
# %%
# drug_table = pd.read_excel('./data/drug.xlsx')
drug_table_an = pd.read_excel('./data/mimiciv_feature_info.xlsx', sheet_name='antibiotic')
drug_table_sa = pd.read_excel('./data/mimiciv_feature_info.xlsx', sheet_name='sedatives_and_analgesics')
drug_table_co = pd.read_excel('./data/mimiciv_feature_info.xlsx', sheet_name='anticoagulant')


prescriptions = pd.read_csv('/data/check_in/EHR_data/MIMIC_III/CSV/PRESCRIPTIONS.csv')
item = pd.read_csv('/data/check_in/EHR_data/MIMIC_III/CSV/D_ITEMS.csv')
labitem = pd.read_csv('/data/check_in/EHR_data/MIMIC_III/CSV/D_LABITEMS.csv')
columns_pre = prescriptions.columns.tolist()
columns_item = item.columns.tolist()
columns_labitem = labitem.columns.tolist()
# drugs = (drug_table['anticoagulant'].to_list()+drug_table['antiplatelet'].to_list())[:-4]
drugs = ['barbital'
        ,'zepam'
        ,'zolam'
        ,'zolpidem'
        ,'propofol'
        ,'dexmedetomidine'
        ,'pentobarbital'
        ,'clonazepam'
        ,'alprazolam'
        ,'estazolam'
        ,'Zolpidem Tartrate']

drug_test_tsv = open('drug_patients_sedative.csv', 'w', newline='', encoding='utf-8')
drug_test = csv.writer(drug_test_tsv, delimiter=',')
drug_test.writerow(columns_pre)

item_test_tsv = open('item_patients_sedative.csv', 'w', newline='', encoding='utf-8')
item_test = csv.writer(item_test_tsv, delimiter=',')
item_test.writerow(columns_item)

labitem_test_tsv = open('labitem_patients_sedative.csv', 'w', newline='', encoding='utf-8')
labitem_test = csv.writer(labitem_test_tsv, delimiter=',')
labitem_test.writerow(columns_labitem)

# import pdb;pdb.set_trace()
for drug in drugs:
    # print(type(drug))
    sql = "select * FROM PRESCRIPTIONS where drug like '%"+ drug + "%' or drug_name_poe like '%"+ drug + "%' or drug_name_generic like '%"+ drug + "%'"
    print(sql)
    conn = connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='mimiciii')
    cursor = conn.cursor()
    cursor.execute(sql)
    data_tmp = cursor.fetchall()
    # print(data_tmp is None)
    if len(data_tmp) != 0:   
        for data_cur in data_tmp:        
            print(data_cur[1], data_cur[2], data_cur[3], data_cur[7], data_cur[8], data_cur[9])
            drug_test.writerow(list(data_cur))
            # import pdb;pdb.set_trace()
for drug in drugs:
    # print(type(drug))
    sql = "select * FROM D_ITEMS where label like '%{}%'" .format(drug)
    print(sql)
    conn1 = connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='mimiciii')
    cursor1 = conn1.cursor()
    cursor1.execute(sql)
    data_tmp = cursor1.fetchall()
    if len(data_tmp) != 0:   
        for data_cur in data_tmp:        
            print(data_cur[1], data_cur[2])
            item_test.writerow(list(data_cur))
            # import pdb;pdb.set_trace()
for drug in drugs:
    # print(type(drug))
    sql = "select * FROM D_LABITEMS where label like '%{}%'" .format(drug)
    print(sql)
    conn1 = connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='mimiciii')
    cursor1 = conn1.cursor()
    cursor1.execute(sql)
    data_tmp = cursor1.fetchall()
    if len(data_tmp) != 0:   
        for data_cur in data_tmp:        
            print(data_cur[1], data_cur[2])
            labitem_test.writerow(list(data_cur))
            # import pdb;pdb.set_trace()

# %%
import pandas as pd
drug = pd.read_csv('drug_patients_sedative.csv')
print(drug.DRUG.unique())
# %%
print(drug.DRUG_NAME_POE.unique())
# %%
print(drug.DRUG_NAME_GENERIC.unique())
# %%
