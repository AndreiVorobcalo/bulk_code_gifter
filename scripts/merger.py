import pandas as pd

def merge_csv_files(user_csv, code_csv):
    users = pd.read_csv(user_csv, header=None) 
    codes = pd.read_csv(code_csv, header=None) 
    codes_list = [code[0] for i,code in codes.iterrows()]
    merged_csv = [[row[0], codes_list[i]] for i,row in users.iterrows()]
    print(merged_csv)
    return(merged_csv)