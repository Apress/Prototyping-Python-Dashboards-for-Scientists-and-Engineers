import pandas as pd
import os


#
# For each year's csv file, and for each apt, apppend the apt's data to the APT/apt
# version


names=[
                  "date",        "facility",     "state",    "region",      "ddso",
                  "class",       "ifri_carrier", "ifri_taxi","ifri_general","ifri_mil",
                  "ifri_total",  "vfri_carrier", "vfri_taxi","vfri_general","vfri_mil",
                  "vfri_total",  "i_carrier",    "i_taxi",   "i_general",   "i_mil",
                  "i_total",     "loc_civ",      "loc_mil",  "loc_total",   "total_ops"
                     ]

def get_csv_year_files():
        # The path for listing items 
        path = './ATADS_CSV/'
        
        # The list of items
        csv_files = os.listdir(path)
        return(csv_files)
        
year_files=get_csv_year_files()

last_year = year_files[-1] #most recent

for yrf in year_files:
    
    print (yrf)
    
    df = pd.read_csv(open('./ATADS_CSV/'+yrf))
    df.columns = names
    
    apt_list = df[df.columns[1]].unique()
    
    for apt in apt_list:
        
        apt_csv = './APT_CSV/'+apt+'.csv'
        dfa = df.loc[df['facility'] == apt]
        dfa.to_csv(apt_csv,mode='a',index=False, header=False)
    
    
    
    




