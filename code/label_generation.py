import numpy as np
import matplotlib.pylab as plt
import pandas as pd


file_list = [
'NEPA_panel_level.dta',
'abortion_panel_level.dta',
'ada_panel_level.dta',
'affirmative_action_panel_level.dta',
'campaign_finance_panel_level.dta',
'capital_punishment_panel_level.dta',
'commercial_speech_panel_level.dta',
'elev_abrogation_panel_level.dta',
'eminent_domain_panel_level.dta',
'epa_panel_level.dta',
'fcc_panel_level.dta',
'first_amend_panel_level.dta',
'homosexual_rights_panel_level.dta',
'nlrb_panel_level.dta',
'obscenity_panel_level.dta',
'piercing_corpveil_panel_level.dta',
'race_discrimination_panel_level.dta',
'sex_discrimination_panel_level.dta',
'sexual_harassment_panel_level.dta',
'takings_panel_level.dta',
'title7_panel_level.dta'
]


def new_file(file_name):
    path = 'data/Circuit_Cases/{}'.format(file_name)
    df = pd.read_stata(path)
    covmatrix = np.cov(df['x_dem'], df['panelvote'])
    df['legal_field'] = file_name[:-16]
    if covmatrix[0][1] > 0:
    ## positive relation with xdem(liberal)
        df['new_label'] = [int(i) for i in df['panelvote'] > 1]
    else:
        df['new_label'] = [int(i) for i in df['panelvote'] <= 1]
    newdf = df[['circuit', 'year', 'month', 'case_name', 'new_label', 'legal_field', 'panelvote', 'x_dem']]
    newdf.to_csv('./data/modified_case/{}_new.csv'.format(file_name[:-4]), index=False)

def main():
    # awk 'FNR > 1' ./data/modified_case/*.csv > ./data/bigfile.csv
    for file_name in file_list:
        new_file(file_name)

if __name__ =='__main__':
    main()