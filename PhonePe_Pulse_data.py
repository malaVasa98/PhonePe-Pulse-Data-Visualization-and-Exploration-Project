# PhonePe Pulse data is available in Github repository.
# Now we need to access it in Python. So we use a git clone to obtain the data and access in Python.
#!git clone https://github.com/PhonePe/pulse.git

# Access the state folders in PhonePe Pulse data
import os
# Path is treated as a string
#path = "pulse/data/aggregated/transaction/country/india/state/"
# To list all the files and directories in the specified directory
#Agg_state_list=os.listdir(path)
# List of all the states in the chosen directory
#Agg_state_list

# Convert the name of the states to match the state name to the state while representing the data in geo-visualization
def change_state_spell(state_lis):
    state_lis = state_lis.str.replace('andaman-&-nicobar-islands','Andaman & Nicobar')
    state_lis = state_lis.str.replace('-',' ')
    state_lis = state_lis.str.title()
    state_lis = state_lis.str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')
    return state_lis
    
# To create an aggregate transaction data in a data format and convert it into a data frame.
# The data for each state for each year is stored in json format
import json
import pandas as pd
path = "pulse/data/aggregated/transaction/country/india/state/"
Agg_state_list=os.listdir(path)

Agg_trans = {
    'State':[],
    'Year':[],
    'Quarter':[],
    'Transaction_type':[],
    'Transaction_count':[],
    'Transaction_amount':[]
}
for i in Agg_state_list:
    path_i = path+i+'/'
    Agg_yr = os.listdir(path_i)
    for j in Agg_yr:
        path_j = path_i+j+'/'
        Agg_yr_lis = os.listdir(path_j)
        for k in Agg_yr_lis:
            path_k = path_j+k
            with open(path_k) as Data:
                D = json.load(Data)
            for z in D["data"]["transactionData"]:
                Name = z["name"]
                Count = int(z["paymentInstruments"][0]["count"])
                Amount = float(z["paymentInstruments"][0]["amount"])
                Agg_trans["State"].append(i)
                Agg_trans["Year"].append(j)
                Agg_trans["Quarter"].append(int(k.strip('.json')))
                Agg_trans["Transaction_type"].append(Name)
                Agg_trans["Transaction_count"].append(Count)
                Agg_trans["Transaction_amount"].append(Amount)
df_agg_trans = pd.DataFrame(Agg_trans)
df_agg_trans.State=change_state_spell(df_agg_trans.State)

df_agg_trans.to_csv('Aggregated_Transaction.csv',index=False)

# Aggregated User table
path = "Phone_Pe/data/aggregated/user/country/india/state/"
Agg_state_list=os.listdir(path)

Agg_user = {
    'State':[],
    'Year':[],
    'Quarter':[],
    'User_brand_name':[],
    'User_count':[],
    'User_count_percentage':[]
}
for i in Agg_state_list:
    path_i = path+i+'/'
    Agg_yr = os.listdir(path_i)
    for j in Agg_yr:
        path_j = path_i+j+'/'
        Agg_yr_lis = os.listdir(path_j)
        for k in Agg_yr_lis:
            path_k = path_j+k
            with open(path_k) as Data:
                U = json.load(Data)
            if U["data"]["usersByDevice"]!=None:
                for z in U["data"]["usersByDevice"]:
                    Name = z["brand"]
                    Count = int(z["count"])
                    Perc = float(z["percentage"])
                    Agg_user["State"].append(i)
                    Agg_user["Year"].append(j)
                    Agg_user["Quarter"].append(int(k.strip('.json')))
                    Agg_user["User_brand_name"].append(Name)
                    Agg_user["User_count"].append(Count)
                    Agg_user["User_count_percentage"].append(Perc)
df_agg_user = pd.DataFrame(Agg_user)
df_agg_user.State=change_state_spell(df_agg_user.State)

df_agg_user.to_csv('Aggregated_User.csv',index=False)

# Map Transaction
path = "Phone_Pe/data/map/transaction/hover/country/india/state/"
Map_state_list=os.listdir(path)

Map_trans = {
    'State':[],
    'Year':[],
    'Quarter':[],
    'District_name':[],
    'Transaction_count_district':[],
    'Total_transaction_value':[]
}
for i in Map_state_list:
    path_i = path+i+'/'
    Map_yr = os.listdir(path_i)
    for j in Map_yr:
        path_j = path_i+j+'/'
        Map_yr_lis = os.listdir(path_j)
        for k in Map_yr_lis:
            path_k = path_j+k
            with open(path_k) as Data:
                D = json.load(Data)
            for z in D["data"]["hoverDataList"]:
                st_ds_name = z["name"]
                Count = int(z["metric"][0]["count"])
                Amount = float(z["metric"][0]["amount"])
                Map_trans["State"].append(i)
                Map_trans["Year"].append(j)
                Map_trans["Quarter"].append(int(k.strip('.json')))
                Map_trans["District_name"].append(st_ds_name)
                Map_trans["Transaction_count_district"].append(Count)
                Map_trans["Total_transaction_value"].append(Amount)

df_map_trans = pd.DataFrame(Map_trans)
df_map_trans.State=change_state_spell(df_map_trans.State)

df_map_trans.to_csv('Map_transaction.csv',index=False)

# Map Users
path ="Phone_Pe/data/map/user/hover/country/india/state/"
Map_state_list=os.listdir(path)

Map_user = {
    'State':[],
    'Year':[],
    'Quarter':[],
    'District_name':[],
    'Registered_users':[],
    'App_opens':[]
}
for i in Map_state_list:
    path_i = path+i+'/'
    Map_yr = os.listdir(path_i)
    for j in Map_yr:
        path_j = path_i+j+'/'
        Map_yr_lis = os.listdir(path_j)
        for k in Map_yr_lis:
            path_k = path_j+k
            with open(path_k) as Data:
                D = json.load(Data)
            for z in D["data"]["hoverData"]:
                ds_name = z
                Reg_cnt = int(D["data"]["hoverData"][z]["registeredUsers"])
                App_ops = int(D["data"]["hoverData"][z]["appOpens"])
                Map_user["State"].append(i)
                Map_user["Year"].append(j)
                Map_user["Quarter"].append(int(k.strip('.json')))
                Map_user["District_name"].append(ds_name)
                Map_user["Registered_users"].append(Reg_cnt)
                Map_user["App_opens"].append(App_ops)
df_map_user = pd.DataFrame(Map_user)
df_map_user.State = change_state_spell(df_map_user.State)

df_map_user.to_csv('Map_user.csv',index=False)

# Top Transaction
path = "Phone_Pe/data/top/transaction/country/india/state/"
Top_state_list = os.listdir(path)
Top_trans_dis = {
    'State':[],
    'Year':[],
    'Quarter':[],
    'District_name':[],
    'Transaction_count_top_dis':[],
    'Total_transaction_top_dis':[]
}
Top_trans_pin = {
    'State':[],
    'Year':[],
    'Quarter':[],
    'PINCODE':[],
    'Transaction_count_top_pin':[],
    'Total_transaction_top_pin':[]
}
for i in Top_state_list:
    path_i = path+i+'/'
    Top_yr = os.listdir(path_i)
    for j in Top_yr:
        path_j = path_i+j+'/'
        Top_yr_lis = os.listdir(path_j)
        for k in Top_yr_lis:
            path_k = path_j+k
            with open(path_k) as Data:
                D = json.load(Data)
            for z in D["data"]["districts"]:
                ds_name = z["entityName"]
                Trans_cnt = int(z["metric"]["count"])
                Trans_amt = float(z["metric"]["amount"])
                Top_trans_dis["State"].append(i)
                Top_trans_dis["Year"].append(j)
                Top_trans_dis["Quarter"].append(int(k.strip('.json')))
                Top_trans_dis["District_name"].append(ds_name)
                Top_trans_dis["Transaction_count_top_dis"].append(Trans_cnt)
                Top_trans_dis["Total_transaction_top_dis"].append(Trans_amt)
            for z in D["data"]["pincodes"]:
                pc = z["entityName"]
                Trans_cnt = int(z["metric"]["count"])
                Trans_amt = float(z["metric"]["amount"])
                Top_trans_pin["State"].append(i)
                Top_trans_pin["Year"].append(j)
                Top_trans_pin["Quarter"].append(int(k.strip('.json')))
                Top_trans_pin["PINCODE"].append(pc)
                Top_trans_pin["Transaction_count_top_pin"].append(Trans_cnt)
                Top_trans_pin["Total_transaction_top_pin"].append(Trans_amt)


df_top_trans_dis = pd.DataFrame(Top_trans_dis)
df_top_trans_dis.State = change_state_spell(df_top_trans_dis.State)

df_top_trans_dis.to_csv('Top_transaction_dis.csv',index=False)

df_top_trans_pin = pd.DataFrame(Top_trans_pin)
df_top_trans_pin.State=change_state_spell(df_top_trans_pin.State)


df_top_trans_pin.to_csv('Top_transaction_pin.csv',index=False)


# Top user
path = "Phone_Pe/data/top/user/country/india/state/"
Top_state_list = os.listdir(path)
Top_user_dis = {
    'State':[],
    'Year':[],
    'Quarter':[],
    'District_name':[],
    'Total_registered_users_dis':[]
}
Top_user_pin = {
    'State':[],
    'Year':[],
    'Quarter':[],
    'PINCODE':[],
    'Total_registered_users_pin':[]
}
for i in Top_state_list:
    path_i = path+i+'/'
    Top_yr = os.listdir(path_i)
    for j in Top_yr:
        path_j = path_i+j+'/'
        Top_yr_lis = os.listdir(path_j)
        for k in Top_yr_lis:
            path_k = path_j+k
            with open(path_k) as Data:
                D = json.load(Data)
            for z in D["data"]["districts"]:
                ds_name = z["name"]
                reg_users = int(z["registeredUsers"])
                Top_user_dis["State"].append(i)
                Top_user_dis["Year"].append(j)
                Top_user_dis["Quarter"].append(int(k.strip('.json')))
                Top_user_dis["District_name"].append(ds_name)
                Top_user_dis["Total_registered_users_dis"].append(reg_users)
            for z in D["data"]["pincodes"]:
                pc = z["name"]
                reg_users = int(z["registeredUsers"])
                Top_user_pin["State"].append(i)
                Top_user_pin["Year"].append(j)
                Top_user_pin["Quarter"].append(int(k.strip('.json')))
                Top_user_pin["PINCODE"].append(int(pc))
                Top_user_pin["Total_registered_users_pin"].append(reg_users)

                
df_top_user_dis = pd.DataFrame(Top_user_dis)
df_top_user_dis.State = change_state_spell(df_top_user_dis.State)

df_top_user_dis.to_csv('Top_user_dis.csv',index=False)

df_top_user_pin = pd.DataFrame(Top_user_pin)
df_top_user_pin.State = change_state_spell(df_top_user_pin.State)

df_top_user_pin.to_csv('Top_user_pin.csv',index=False)







