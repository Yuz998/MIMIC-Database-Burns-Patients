# %%
import pandas as pd
ROOT = '/data/check_in/EHR_data/MIMIC-IV/'
diag_item = pd.read_csv(ROOT + 'd_icd_diagnoses.csv')
diag_item.info()
# %%
diag_burn = pd.read_excel(u'2度_mimic4.xlsx')
# diag_burn2 = pd.read_excel(u'2度_mimic4.xlsx')
diag = pd.read_csv(ROOT + 'diagnoses_icd.csv')
diag.dropna(subset=['icd_code'], axis=0, inplace=True)
# %%
diag_burn['icd_code'] = diag_burn['icd_code'].astype(str).apply(lambda x: str(x).strip())
# diag_burn2['icd_code'] = diag_burn2['icd_code'].apply(lambda x: str(x).strip())
diag['icd_code'] = diag['icd_code'].astype(str).apply(lambda x: str(x).strip())
diag_item['icd_code']=diag_item['icd_code'].astype(str).apply(lambda x: str(x).strip())
# %%
burn_id = diag_burn['icd_code'].to_list()
diag_pat = diag[diag['icd_code'].isin(burn_id)]

# %%
hadms = diag_pat['hadm_id'].to_list()
diag_all = diag[diag['hadm_id'].isin(hadms)]
diag_info = pd.merge(diag_all, diag_item, on=['icd_code', 'icd_version'], how='left')
diag_info['2_flag'] = (diag_info['icd_code'].isin(burn_id)).astype(int)
# %%
diag_info
# %%
diag_item[diag_item['icd_code'] == 'V3001']
# %%
diag[diag['subject_id'] == 16938846]
# %%
diag_info.to_csv('diag_2-14.csv', index=False)






# %%
diag_max_seq = diag.copy()
diag_max_seq.sort_values(by=['subject_id', 'hadm_id', 'seq_num'], inplace=True)
# diag.sort_values(by=['subject_id', 'hadm_id', 'seq_num'], inplace=True)
diag_max_seq.drop_duplicates(subset=['hadm_id'], keep='last', inplace=True)
# %%
diag_max_seq['seq_num_HALF'] = diag_max_seq['seq_num'] / 2
diag_max_seq['seq_num_THIRD'] = diag_max_seq['seq_num'] / 3
diag_max_seq.drop(labels=['icd_code', 'seq_num'], inplace=True, axis=1)
# %%
diag_pat_0 = pd.merge(diag_pat, diag_max_seq, on=['subject_id', 'hadm_id'], how='left')
# %%
diag_pat_0['half_flag'] = diag_pat_0.apply(lambda row: 1 if row['seq_num'] <= row['seq_num_HALF'] else 0, axis=1)
diag_pat_0['third_flag'] = diag_pat_0.apply(lambda row: 1 if row['seq_num'] <= row['seq_num_THIRD'] else 0, axis=1)

# %%
diag_pat_0.sort_values(by=['subject_id', 'hadm_id', 'seq_num'], inplace=True)
diag_pat_0.drop_duplicates(subset=['subject_id', 'hadm_id'], keep='first', inplace=True)
# %%
diag_pat_flag = diag_pat_0[['subject_id', 'hadm_id', 'half_flag', 'third_flag']]
# %%
task1 =  diag[diag['hadm_id'].isin(diag_pat_0['hadm_id'])]
# %%
task1
# %%
task1['burn_flag'] = (task1['icd_code'].isin(diag_burn['icd_code'].to_list())).astype(int)
# %%
task1 = pd.merge(task1, diag_item, on=['icd_code'], how='left')

task1.to_csv('first_task_1.csv', index=False)

# %%
task1 = pd.merge(task1, diag_pat_flag, on=['subject_id', 'hadm_id'], how='left')


#%%
diag_pat_2 = diag_pat
# %%
task2 = diag[diag['hadm_id'].isin(diag_pat_2['hadm_id'])]
# %%
task_2 = task2[task2['icd_code'].isin(diag_burn2['icd_code'])]
# %%
task2['burn_2_flag'] = (task2['icd_code'].isin(diag_burn2['icd_code'].to_list())).astype(int)

# %%
t2 = pd.merge(task_2, diag_item, on=['icd_code'], how='left')
# %%
t2.to_csv('second_task-1.csv', index=False)
# %%
task_2.shape