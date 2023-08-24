#!pip install streamlit

import numpy as np
import pandas as pd
import requests
import json
import seaborn as sns
#import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import datetime


# 2022 MSSP ACO results
resp = requests.get("https://data.cms.gov/data-api/v1/dataset/73b2ce14-351d-40ac-90ba-ec9e1f5ba80c/data")
df22 = pd.read_json(json.dumps(resp.json()))


# 2021 MSSP ACO results
resp = requests.get("https://data.cms.gov/data-api/v1/dataset/73b2ce14-351d-40ac-90ba-ec9e1f5ba80c/data")
df21 = pd.read_json(json.dumps(resp.json()))
#print(df.head())


#2020 MSSP ACO results
resp4 = requests.get("https://data.cms.gov/data-api/v1/dataset/8f073013-9db0-4b12-9a34-5802bdabbdfe/data")
df20 = pd.read_json(json.dumps(resp4.json()))
#print(df20.head())
df20.rename(columns={"aco_id": "ACO_ID"},inplace=True)
df20.rename(columns={"Sav_rate":"Sav_Rate"},inplace=True)

#2019 MSSP ACO results
resp5 = requests.get("https://data.cms.gov/data-api/v1/dataset/9c3a4c69-7d00-4307-9b6f-a080dc90417e/data")
df2019 = pd.read_json(json.dumps(resp5.json()))
#print(df19.head())


#2018 MSSP ACO results
resp6 = requests.get("https://data.cms.gov/data-api/v1/dataset/80c86127-8839-4f35-b87b-aa37664afd19/data")
df18 = pd.read_json(json.dumps(resp6.json()))
#print(df18.head())
df18.rename(columns={"Sav_rate":"Sav_Rate"},inplace=True)
df18.rename(columns={"aco_id": "ACO_ID"},inplace=True)


df2019.rename(columns={"aco_id": "ACO_ID", "aco_name":"ACO_Name","aco_state":"ACO_State"},inplace=True)
df2019.rename(columns={"sav_rate":"Sav_Rate","capann_inp_all":"CapAnn_INP_All","maxsharerate":"MaxShareRate",
"capann_inp_s_trm":"CapAnn_INP_S_trm",  "capann_inp_l_trm":"CapAnn_INP_L_trm", 
"capann_inp_rehab":"CapAnn_INP_Rehab",  "capann_inp_psych":"CapAnn_INP_Psych",  
"capann_hsp":"CapAnn_HSP",  "capann_snf":"CapAnn_SNF", "capann_hha":"CapAnn_HHA", 
 "adm":"ADM",  "adm_s_trm":"ADM_S_Trm",  "adm_l_trm":"ADM_L_Trm", 
 "adm_rehab":"ADM_Rehab", "p_edv_vis":"P_EDV_Vis", 
 "p_edv_vis_hosp":"P_EDV_Vis_HOSP","p_em_total":"P_EM_Total", 
 "p_em_pcp_vis":"P_EM_PCP_Vis",  "p_em_sp_vis":"P_EM_SP_Vis", 
 "finalsharerate":"FinalShareRate","gensaveloss":"GenSaveLoss","p_snf_adm":"P_SNF_ADM",
 'aco1':'ACO1', 'aco2':"ACO2", 'aco3':"ACO3", 'aco4':"ACO4", 'aco5':"ACO5", 'aco6':"ACO6", 'aco7':"ACO7", 'aco34':"ACO34",'aco45':"ACO45",'aco46':"ACO46",'aco8':"ACO8", 'aco38':"ACO38",'aco43':'ACO43',
 'aco13':'ACO13','aco14':'ACO14','aco17':'ACO17','aco18':'ACO18','aco19':'ACO19','aco20':'ACO20','aco42':'ACO42',
"n_ab":"N_AB",
 "n_ben_race_white":"N_Ben_Race_White",
"n_ben_race_black":"N_Ben_Race_Asian",
"n_ben_race_asian":"N_Ben_Race_Asian",
"n_ben_race_hisp":"N_Ben_Race_Hisp",
"n_ben_race_native":"N_Ben_Race_Native",
"n_ben_race_other":"N_Ben_Race_Other",
"qualscore":"QualScore",
 'aco40':'ACO40','aco27':'ACO27',  'aco28':'ACO28' },inplace=True) 

#df19.to_csv(r'D:\Downloads\19out.csv', index=False)
df19=df2019    
#df19=pd.read_csv(r'D:\Data\Analyze CMS data/19out.csv')  

#'MaxShareRate' not in 22
convn = ['P_EM_PCP_Vis','CapAnn_HHA','FinalShareRate','CapAnn_SNF', 'Sav_Rate','CapAnn_INP_S_trm']
convn1=[]
convn2=['df18','df19','df20','df21','df22']


df22=df22.rename(columns={'Sav_rate': "Sav_Rate"})
df22['Sav_Rate']=df22['Sav_Rate'].str.replace("%","")
df21=df21.rename(columns={'Sav_rate': "Sav_Rate"})
df21['Sav_Rate']=df21['Sav_Rate'].str.replace("%","")
df20['Sav_Rate']=df20['Sav_Rate']*100
df18['Sav_Rate']=df18['Sav_Rate']*100
df19['Sav_Rate']=df19['Sav_Rate']*100
df21['QualScore']=df21['QualScore'].str.replace("%","")
df18['QualScore']=df18['QualScore']*100
df18['FinalShareRate']=df18['FinalShareRate']*100
df19['FinalShareRate']=df19['FinalShareRate']*100
df21['FinalShareRate']=df21['FinalShareRate'].str.replace("%","")
df18['QualScore']=df18['QualScore']/100
df22['QualScore']=df22['QualScore'].str.replace("%","")
 

for i in convn:
  if df22[i].dtype==object:
    convn1.append(i)

conv2=['df20','df19','df18','df21','df22']
for i in convn:
  for j in conv2:
    try:
      j[i]=j[i].str.replace(",","")
    except:
      continue
    try:
      j[i]=j[i].str.replace("%","")
    except:
      continue
    try:
      j[i]=j[i].apply(pd.to_numeric, errors='coerce')
    except:
      continue

df21['year']=2021
df19['year']=2019
df18['year']=2018
df20['year']=2020
df22['year']=2022


df18.rename(columns={"aco_id": "ACO_ID",
"ACO13":"QualityID318",
"ACO14":"QualityID_110",
"ACO17":"QualityID_226",
"ACO18":"QualityID_134_WI",
"ACO19":"QualityID_113",
"ACO20":"QualityID_112","ACO42":"QualityID_438",
"ACO40":"QualityID_370",
"ACO27":"QualityID_001_WI","ACO28":"QualityID_236_WI"},inplace=True)


df19.rename(columns={"aco_id": "ACO_ID","Sav_rate":"Sav_Rate",
"ACO13":"QualityID318",
"ACO14":"QualityID_110",
"ACO17":"QualityID_226",
"ACO18":"QualityID_134_WI",
"ACO19":"QualityID_113",
"ACO20":"QualityID_112","ACO42":"QualityID_438",
"ACO40":"QualityID_370",
"ACO27":"QualityID_001_WI","ACO28":"QualityID_236_WI"},inplace=True)

df20.rename(columns={"aco_id": "ACO_ID",
"ACO13":"QualityID318",
"ACO14":"QualityID_110",
"ACO17":"QualityID_226",
"ACO18":"QualityID_134_WI",
"ACO19":"QualityID_113",
"ACO20":"QualityID_112","ACO42":"QualityID_438",
"ACO40":"QualityID_370",
"ACO27":"QualityID_001_WI","ACO28":"QualityID_236_WI"},inplace=True)

df21.rename(columns={"aco_id": "ACO_ID"},inplace=True)
 
df22['ACO_year']= df22['ACO_ID']+"2022"
df21['ACO_year']= df21['ACO_ID']+"2021"
df20['ACO_year']= df20['ACO_ID']+"2020"
df19['ACO_year']= df19['ACO_ID']+"2019"
df18['ACO_year']= df18['ACO_ID']+"2018"

#there is a duplicate problem which creates a problem with concatenate
a=df19.columns
import collections
print([item for item, count in collections.Counter(a).items() if count > 1])
df19=df19.drop(['N_Ben_Race_Asian'], axis=1)

df18=df18.set_index('ACO_year')
df19=df19.set_index('ACO_year')
df20=df20.set_index('ACO_year')
df21=df21.set_index('ACO_year')
df22=df22.set_index('ACO_year')


frames = [ df18,df19, df20,df21,df22] #df19 is creating problem
dfmerge = pd.concat(frames,axis=0)

dfmerge=dfmerge.sort_values(by=['ACO_ID'])

#"MaxShareRate",

dfmerge=dfmerge[[
'ACO_Name','ACO_ID','year',
'ACO_State',
"Sav_Rate",
"CapAnn_INP_All",
"CapAnn_INP_S_trm",  
"CapAnn_INP_L_trm", 
"CapAnn_INP_Rehab",  
"CapAnn_INP_Psych",  
"CapAnn_HSP",  
"CapAnn_SNF",  
"CapAnn_HHA",  
"ADM",  
"ADM_S_Trm",  
"ADM_L_Trm", 
"ADM_Rehab", 
"P_EDV_Vis",  
"P_EDV_Vis_HOSP",
"P_EM_Total",  
"P_EM_PCP_Vis",  
"P_EM_SP_Vis",  
"GenSaveLoss",
"FinalShareRate",
"P_SNF_ADM",
"QualScore",
"ACO1",      
"ACO2", 
"ACO3", 
"ACO4", 
"ACO5", 
"ACO6", 
"ACO7", 
"ACO34",
"ACO45",
"ACO46",
"ACO8",
"ACO38",
"ACO43",
"QualityID318",
"QualityID_110",
"QualityID_226",
"QualityID_134_WI",
"QualityID_113",
"QualityID_112","QualityID_438",
"QualityID_370",
"QualityID_001_WI","QualityID_236_WI", 'N_AB', 'N_PCP', 'N_Ben_Race_Asian', 'N_Ben_Race_Hisp','N_Ben_Race_Other' ,'N_Ben_Race_Hisp', 'N_Ben_Race_Asian','N_Ben_Race_White'
]]

dfmerge.to_csv(r'D:\CMS_ACO_2023\df2018-2023.csv', index=False)
