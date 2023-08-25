import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib as plt
import requests
import json
import regex as re
import streamlit as st

#downloaded ACO data
df=pd.read_csv("https://raw.githubusercontent.com/mangospace/ACO_Perf_2023/main/Performance_Year_Financial_and_Quality_Results_2022.csv")  
#created using ACO_address.py; data stored in aco_addresses_geocoded.csv
dataz=pd.read_csv("https://raw.githubusercontent.com/mangospace/ACO_Perf_2023/main/aco_addresses_geocoded.csv")  
dataz=dataz[['ACO_ID',"ACO_State","lat","long"]]
dataz=dataz.drop_duplicates()
dataz=dataz.reset_index()


df=df.merge(dataz, left_on='ACO_ID', right_on='ACO_ID')


df['ACO_Name']= df['ACO_Name'].str.replace("Accountable Care Organization","")
df['ACO_Name']= df['ACO_Name'].str.replace("Aco","")
df['ACO_Name']= df['ACO_Name'].str.replace("Accountable Care Network","")
df['ACO_Name']= df['ACO_Name'].str.replace("Clinically Integrated Network","CIN")
df['ACO_Name']= df['ACO_Name'].str.replace("Independent Practice Association","IPA")
df['ACO_Name']= df['ACO_Name'].str.replace("Medical Center","Center")
df['ACO_Name']= df['ACO_Name'].str.replace(" of "," ")
df['ACO_Name']= df['ACO_Name'].str.replace(" Of "," ")
df['ACO_Name']= df['ACO_Name'].str.replace("The ","")

df['ACO_Name']= df['ACO_Name'].str.replace(" llc","")
df['ACO_Name']= df['ACO_Name'].str.replace("LLC","")
df['ACO_Name']= df['ACO_Name'].str.replace(", PLLC","")
df['ACO_Name']= df['ACO_Name'].str.replace(", L.L.C.","")
df['ACO_Name']= df['ACO_Name'].str.replace(" Inc.","")
df['ACO_Name']= df['ACO_Name'].str.replace(" INC.","")
df['ACO_Name']= df['ACO_Name'].str.replace(" Inc","")
df['ACO_Name']= df['ACO_Name'].str.replace(" INC","")
df['ACO_Name']= df['ACO_Name'].str.replace(", P.C.","")
df['ACO_Name']= df['ACO_Name'].str.replace(",","")
df['ACO_Name']= df['ACO_Name'].str.replace(".","")
df['ACO_Name']= df['ACO_Name'].str.replace("MercyOne ACO","Mercy")
df['ACO_Name']= df['ACO_Name'].str.replace("Quality Network","")
df['ACO_Name']= df['ACO_Name'].str.replace("Health Network","")
df['ACO_Name']= df['ACO_Name'].str.replace("Quality Care","QC")
df['ACO_Name']= df['ACO_Name'].str.replace("Quality Partners","QP")
df['ACO_Name']= df['ACO_Name'].str.replace("Quality Alliance","QA")
df['ACO_Name']= df['ACO_Name'].str.replace("QC Alliance","QA")
df['ACO_Name']= df['ACO_Name'].str.replace("Health Alliance","HA")
df['ACO_Name']= df['ACO_Name'].str.replace("Healthcare Alliance","HA")
df['ACO_Name']= df['ACO_Name'].str.replace("Health Care Alliance","HA")
df['ACO_Name']= df['ACO_Name'].str.replace("Provider Alliance","PA")
df['ACO_Name']= df['ACO_Name'].str.replace("Group","")
df['ACO_Name']= df['ACO_Name'].str.replace("Network","")
df['ACO_Name']= df['ACO_Name'].str.replace("Healthcare","Health")
df['ACO_Name']= df['ACO_Name'].str.replace("ACO-ES","")
df['ACO_Name']= df['ACO_Name'].str.strip()
#df['ACO_Name']= df['ACO_Name'].str.title()

df=df.rename(columns={"Measure_484": "Measure_MCC1","Sav_rate":"Sav_Rate"})
df['QualScore']=df['QualScore'].str.replace("%","")
df['Sav_Rate']=df['Sav_Rate'].str.replace("%","")


df['ACO_identifier1']= df['ACO_Name']+"- "+df['ACO_State']
convn = ['Measure_MCC1','P_EM_PCP_Vis','Perc_Dual','Measure_479','CapAnn_HHA','FinalShareRate','QualityID_113','QualityID_112', 'N_AB', 'N_PCP', 'N_Ben_Race_Black', 'N_Ben_Race_Hisp','N_Ben_Race_Other' ,'QualScore',
         'N_Ben_Race_Native', 'N_Ben_Race_Asian','N_Ben_Race_White', 'Sav_Rate','P_EDV_Vis','P_EDV_Vis_HOSP','ADM_Rehab']
convn1=[]
for i in convn:
  if df[i].dtype==object:
    convn1.append(i)

for i in convn1:
  df[i]=df[i].str.replace(",","")
  df[i]=df[i].str.replace("%","")
  df[i]=df[i].str.replace("*","0")
  df[i]=df[i].apply(pd.to_numeric, errors='coerce')



df['ptperpcp']=pd.to_numeric(df['N_AB'])/pd.to_numeric(df['N_PCP'])
df['AfAmHispshare1']= (df['N_Ben_Race_Black'].add( df['N_Ben_Race_Hisp'], fill_value=0)) / (df['N_Ben_Race_Black']+ df['N_Ben_Race_Hisp'] + df['N_Ben_Race_Other'] + df['N_Ben_Race_Native'] + df['N_Ben_Race_Asian'] + df['N_Ben_Race_White']).astype(float)

print(df['AfAmHispshare1'])

#PCP visits for all the ACOs
P_EM_PCP_Vis_med=df['P_EM_PCP_Vis'].median() #3714.0
#PCP visits for high revenue ACOs
P_EM_PCP_Vis_medH=df.loc[(df['Rev_Exp_Cat'] == "High Revenue")]['P_EM_PCP_Vis'].median() #3315

#ADK  for all the ACOs
ADM_S_Trm_med=df['ADM_S_Trm'].median() #237.0
ADM_S_Trm_mean=round(df['ADM_S_Trm'].mean() , 2) #2
ADM_S_Trm_min=df['ADM_S_Trm'].min() #112
#ADK  for hospital ACOs
ADM_S_Trm_medH=df.loc[(df['Rev_Exp_Cat'] == "High Revenue")]['ADM_S_Trm'].median() #238.5
ADM_S_Trm_minH=df.loc[(df['Rev_Exp_Cat'] == "High Revenue")]['ADM_S_Trm'].min() #112

#ED visits
df['ED_V']=df['P_EDV_Vis'] + df['P_EDV_Vis_HOSP']
#df['ED_V']=df['P_EDV_Vis', 'P_EDV_Vis_HOSP'].sum(axis = 1, skipna = True)
df['admfrac']=round(df['P_EDV_Vis_HOSP'] *100/ (df['P_EDV_Vis']+df['P_EDV_Vis']),2)
ED_V_med= round(df['ED_V'].median() , 2)
ED_V_medH=round(df.loc[(df['Rev_Exp_Cat'] == "High Revenue")]['ED_V'].median() , 2)
admfrac_med= round(df['admfrac'].median() , 1)
admfrac_medH=round(df.loc[(df['Rev_Exp_Cat'] == "High Revenue")]['admfrac'].median() , 1)


#SNF ADK  for hospital ACOs
P_SNF_ADM_med=df['P_SNF_ADM'].median() #45
P_SNF_ADM_medH=df.loc[(df['Rev_Exp_Cat'] == "High Revenue")]['P_SNF_ADM'].median() #45
P_SNF_ADM_min=df['P_SNF_ADM'].min() #15
P_SNF_ADM_minH=df.loc[(df['Rev_Exp_Cat'] == "High Revenue")]['P_SNF_ADM'].min() #18

#SNF LOS  for hospital ACOs
SNF_LOS_med=df['SNF_LOS'].median() #26
SNF_LOS_medH=df.loc[(df['Rev_Exp_Cat'] == "High Revenue")]['SNF_LOS'].median() #26
SNF_LOS_min=df['SNF_LOS'].min() #19
SNF_LOS_minH=df.loc[(df['Rev_Exp_Cat'] == "High Revenue")]['SNF_LOS'].min() #19

#Rehab Hospital LOS  for hospital ACOs
ADM_Rehab_med=df['ADM_Rehab'].median() #12
df.loc[(df['Rev_Exp_Cat'] == "High Revenue")]['ADM_Rehab'].median() #11
ADM_Rehab_min=df['ADM_Rehab'].min() #12
df.loc[(df['Rev_Exp_Cat'] == "High Revenue")]['ADM_Rehab'].min() #11


#Readmissions
Measure_479_med=df['Measure_479'].median() * 100 #.1553
Measure_479_medH=df.loc[(df['Rev_Exp_Cat'] == "High Revenue")]['Measure_479'].median() * 100 #.15325
Measure_479_min=df['Measure_479'].min() #.1553
Measure_479_minH=df.loc[(df['Rev_Exp_Cat'] == "High Revenue")]['Measure_479'].min()#.15325

#admissions of complex patients
Measure_MCC1_med=df['Measure_MCC1'].median() #33.94
Measure_MCC1_medH=df.loc[(df['Rev_Exp_Cat'] == "High Revenue")]['Measure_MCC1'].median() #34.59
Measure_MCC1_min=df['Measure_MCC1'].min() #17.64
Measure_MCC1_minH=df.loc[(df['Rev_Exp_Cat'] == "High Revenue")]['Measure_MCC1'].min() #23.04


#Baseline year RAF Aged non duals
df['CMS_HCC_RiskScore_AGND_BY3'].median() #1.01
df.loc[(df['Rev_Exp_Cat'] == "High Revenue")]['CMS_HCC_RiskScore_AGND_BY3'].median() #1.0025

#Performance year RAF Aged non duals
df['CMS_HCC_RiskScore_AGND_PY'].median() #1.016
df.loc[(df['Rev_Exp_Cat'] == "High Revenue")]['CMS_HCC_RiskScore_AGND_PY'].median() #1.0005

df1=df

df1.loc[df1['ACO_ID']=="A1001",'ACO_Name'].values[0]

st.title('ACO 2022 Performance Explorer V0.0')
st.header("Please don't be deterred by ugly red box(es). They disappear as you enter required fields.")
st.caption('Made with \u2764\uFE0F @manas8u in Python and Streamlit')
st.caption('Understand the somewhat \U0001F479 nature of this version')
st.caption('Please share your feedback and suggestions. DM @manas8u')

st.write("This is a analytics report of 2021 performance year to help ACOs understand and contextualize their performance.")
st.write('This report is customized by entering ACO of interest.')
st.write('Overall ACO performance statistics are available towards the end of the report.')
st.write('To tailor the comparison, what might be your ACO of interest. You can look up your ACO_ID on CMS  website. Please toggle between Basic filtering and Advanced filtering till you can identify ACO that you are looking for.') 
"""https://data.cms.gov/medicare-shared-savings-program/performance-year-financial-and-quality-results/data"""
val3 = st.text_input("What is your ACO ID?")
if len(val3) != 0:
         val3=val3.upper()

         ACO_head1= df1.loc[df1['ACO_ID']==val3,'ACO_Name'].values[0]
         st.subheader(f"You have choosen {val3} : {ACO_head1}")
         ACO_head= ACO_head1[0:10]
         st.subheader("To tailor the comparison, its important to identify comparable ACOs")

         st.write("If ACO participants spent >35% of total Medicare Parts A and B Fee For Service revenue for the performance year, in your ACO participants CMS considers your ACO as 'high revenue'.")
         st.write("If ACO participants spent <35% of total Medicare Parts A and B Fee For Service revenue for the performance year, , in your ACO participants CMS considers your ACO as 'low revenue'.")
         st.write("To tailor the comparison, its useful to know what kind of ACO you might be interested in comparing the ACO of interest with. Hospitals might be part of your ACO, if your ACO incorporates clinicians that are employed by hospital. In the ACO that you are interested to analyze, are hospitals included.  Please enter yes if hospitals are part of your ACO")
         val1 = st.text_input("Are Hospitals part of your ACO (use 'yes' or 'no' please)?")
         val1=val1.upper()

         st.subheader(f"ACO of interest is: {val3}")
         if val1=="YES":
             st.subheader(f"{ACO_head} is a 'High Revenue' ACO")
         if val1=="NO":
             st.subheader(f"{ACO_head} is a 'Low Revenue' ACO")

         # choose hospital based or non hospital based ACOs
         if val1=="YES":
           df1= df1.loc[(df1['Rev_Exp_Cat'] == "High Revenue") |(df1['ACO_ID'] == val3)]
         if val1=="NO":
           df1= df1.loc[(df1['Rev_Exp_Cat'] == "Low Revenue")| (df1['ACO_ID'] == val3)]

         st.write("You can choose ACOs based on the State with most of your members or you can choose ACOs with ACO address closest to the address of your ACO.You might choose this strategy if the ACO of interest is in a small state or is close to state boundary.")
         """WARNING: This strategy is less than optimal because it identifies closest ACOs using postal address with CMS.!"""
         """"WARNING: This strategy fails with Aledade ACOs which use a common postal address.!"""
         st.write("What strategy would you like to use to identify comparable ACOs?")
         valstrat = st.text_input("Please enter 1 if you would use State based strategy to identify comparators or 2 if you would like to use geography based strategy): ")

         if valstrat=="1":
             st.write("To tailor the comparison, its useful to identify population of interest. Please use two letter identifier please. e.g. if most of your ACO members live in Pennsylvania, enter PA")
             val = st.text_input("What State is majority/most of your ACO population(use two letter state identifier please)?")
             val=val.upper()
         if len(valstrat) != 0:
         
                  if valstrat=="1":
                      st.subheader(f"ACO of interest is: {val3}")
                      st.subheader(f"{val3} is 'High Revenue' ACO: {val1}")
                      st.subheader(f"'Home' State of interest: {val}")
                      df3=df1.loc[df1['ACO_State'].str.contains(val) | (df1['ACO_ID'] == val3)]

                  lated1=df1.loc[df1['ACO_ID'] == val3]
                  lat1=lated1.iloc[0]['lat']
                  lon1=lated1['long']

                  def distance(row):
                      lat2= float(row['lat']) 
                      lon2= float(row['long']) 
                      radius = 6371 # km
                      dlat = math.radians(lat2-lat1)
                      dlon = math.radians(lon2-lon1)
                      a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                          * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
                      c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                      d = radius * c
                      return d

                  if valstrat=="2":
                    import math
                    df1['distance']=df1.apply(distance,axis=1)
                    df1=df1.sort_values(by=['distance'])
                    df4=df1.head(9)
                    df5=df1.loc[(df1['ACO_ID'] == val3)]
                    df3= pd.concat([df4, df5])


                  if len(df3)> 10:
                    st.write("There are more than 10 ACOs in the state of your interest which makes comparisons challenging.")
                    st.write("Would you like to compare your ACO to the best performing ACO in your state or a random sample of 9 ACOs ?")
                    st.subheader("Please note that random sample of ACOs would remain the same in case you want to return to this report later.")
                    #add + average of ACOs in your state
                    valbest = st.text_input("Please enter yes if you would like to compare to the 9 best performing ACOs.")
                    valbest=valbest.upper()
                    if valbest=="NO":
                        df4=df3.sample(n = 9, random_state=1)
                        if val3 in list(df4['ACO_ID']):
                            df4=df3.sample(n = 8, random_state=2)
                        df5=df1.loc[(df1['ACO_ID'] == val3)]
                        df3= pd.concat([df4, df5])

                    if valbest=="YES":
                        df3=df3.sort_values(by=['Sav_Rate'])
                        df4=df3.head(9)
                        if val3 in list(df4['ACO_ID']):
                            df3=df3.head(10)
                        else:
                            df5=df1.loc[(df1['ACO_ID'] == val3)]
                            df3= pd.concat([df4, df5])

                  df3=df3.drop_duplicates(subset=['ACO_ID'])
                  df3['Sav_Rate']=df3['Sav_Rate'].round(2)
                  st.subheader("Savings Rates of your ACO in comparison with others")
                  if val1=="YES":
                      st.write(f"This list has 'High Revenue' ACOs only")
                  if val1=="NO":
                      st.write(f"This list has 'Low Revenue' ACOs only")
                  df.style.hide_index()
                  df3=df3.sort_values(by=['Sav_Rate'],ascending=False)
                  st.dataframe(df3[['ACO_ID','ACO_Name','ACO_State','Sav_Rate']])

                  ptperpcp_int=int(df3.loc[df3['ACO_ID']==val3,'ptperpcp'].values[0])
                  ptperpcp_ran=df3.ptperpcp.max()-df3.ptperpcp.min()
                  ptperpcpl=int(round(df3.ptperpcp.min()-ptperpcp_ran/10,0))
                  ptperpcph=int(round(df3.ptperpcp.max()-ptperpcp_ran/10,0))
                  #bat=[*range(ptperpcpl,ptperpcph,5)]

                  st.subheader("Member Attribution of PCPs")
                  st.caption(f"Orange line indicates ACO ID: {val3}")
                  from matplotlib.ticker import MaxNLocator
                  import matplotlib.pyplot as plt
                  (n, bins, patches) = plt.hist(df3.ptperpcp, bins=5, label='hst',edgecolor='black', linewidth=0.5)
                  x1, y1 = [ptperpcp_int, ptperpcp_int], [0, max(n)+1]
                  fig,ax = plt.subplots(1,1)
                  ax.hist(df3.ptperpcp, bins = 5,edgecolor='black', linewidth=0.5)
                  ax.set_title("ACO members attributed per ACO PCP")
                  #ax.set_xticks([25,50,75,100,125,150,175.200])
                  ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                  #ax.set_yticks([25,50,75,100,125,150,175.200])
                  ax.set_xlabel('Number of members ')
                  ax.set_ylabel('No. of ACOs in comparison group')
                  plt.plot(x1, y1, marker = 'o')
                  plt.show()
                  st.pyplot(fig)


                  st.subheader("Dual(Medicaid-Medicare) prevalence among ACO members")
                  st.write ("Indicator of SDOH needs")
                  st.caption(f"Orange line indicates ACO ID: {val3}")

                  fig,ax = plt.subplots(1,1)
                  (n, bins, patches) = ax.hist(df3.Perc_Dual, bins=5, label='hst',edgecolor='black', linewidth=0.5)
                  Perc_Dual_int=int(df3.loc[df3['ACO_ID']==val3,'Perc_Dual'].values[0])
                  x1, y1 = [Perc_Dual_int, Perc_Dual_int], [0, max(n)+1]
                  #ax.hist(df3.Perc_Dual, bins = 5 ,edgecolor='black', linewidth=0.5)
                  ax.set_title("Prevalence of beneficiaries challenged by SDOH")
                  ax.set_xlabel('Percentage of beneficiaries that were duals for => 1 month')
                  ax.set_ylabel('No. of ACOs in comparison group')
                  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                  plt.plot(x1, y1, marker = 'o')
                  plt.show()
                  st.pyplot(fig)

                  st.subheader("Racial diversity among ACO members")
                  st.caption(f"Orange line indicates ACO ID: {val3}")
                  try:  
                  df3.AfAmHispshare1=df3.AfAmHispshare1*100
                  fig,ax = plt.subplots(1,1)
                  (n, bins, patches) = ax.hist(df3.AfAmHispshare1 , bins=5, label='hst',edgecolor='black', linewidth=0.5)
                  AfAmHispshare1_int=int(df3.loc[df3['ACO_ID']==val3,'AfAmHispshare1'].values[0])
                  x1, y1 = [AfAmHispshare1_int, AfAmHispshare1_int], [0, max(n)+1]
                  #ax.hist(df3.Perc_Dual, bins = 5 ,edgecolor='black', linewidth=0.5)
                  ax.set_title("Beneficiaries that are African American or Hispanic")
                  ax.set_xlabel('Percentage of beneficiaries that are African American or Hispanic')
                  ax.set_ylabel('No. of ACOs in comparison group')
                  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                  plt.plot(x1, y1, marker = 'o')
                  plt.show()
                  st.pyplot(fig)


                  st.subheader("Primary Care Intensity")
                  st.caption(f"Orange line indicates ACO ID: {val3}")

                  P_EM_PCP_Vis_int=int(df3.loc[df3['ACO_ID']==val3,'P_EM_PCP_Vis'].values[0])
                  fig,ax = plt.subplots(1,1)
                  (n, bins, patches) = ax.hist(df3.P_EM_PCP_Vis, bins=5, label='hst',edgecolor='black', linewidth=0.5)
                  x1, y1 = [P_EM_PCP_Vis_int, P_EM_PCP_Vis_int], [0, max(n)+1]
                  #ax.hist(df3.P_EM_PCP_Vis, bins = 5,edgecolor='black', linewidth=0.5)
                  ax.set_title("PCP visits per 1000 ACO members ")
                  #ax.set_xticks([2000,2500,3000,3500,4000,4500.5000])
                  ax.set_xlabel('Number of visits per 1000 members')
                  ax.set_ylabel('No. of ACOs in comparison group')
                  ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                  plt.plot(x1, y1, marker = 'o')
                  plt.show()
                  st.pyplot(fig)

                  st.subheader("Inpatient Utilization in ACO")
                  st.caption(f"Orange line indicates ACO ID: {val3}")

                  ADM_S_Trm_int=int(df3.loc[df3['ACO_ID']==val3,'ADM_S_Trm'].values[0])
                  fig,ax = plt.subplots(1,1)
                  (n, bins, patches) = ax.hist(df3.ADM_S_Trm, bins=5, label='hst',edgecolor='black', linewidth=0.5)
                  x1, y1 = [ADM_S_Trm_int, ADM_S_Trm_int], [0, max(n)+1]
                  ax.set_title("ACO Hospital Utilization")
                  ax.set_xlabel('Number of admissions per 1000 members')
                  ax.set_ylabel('No. of ACOs in comparison group')
                  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                  plt.plot(x1, y1, marker = 'o')
                  plt.show()
                  st.pyplot(fig)

#                 dfmerge=pd.read_csv('https://raw.githubusercontent.com/mangospace/ACO-2022-Performance-Explorer-V1/main/df2018-2022.csv')
                  dfmerge=pd.read_csv('https://raw.githubusercontent.com/mangospace/ACO_Perf_2023/main/df2018-2023.csv')
                  df_sav=dfmerge[['ACO_Name','year','ADM_S_Trm','ACO_ID']]

                  mat=list(df3.ACO_ID)

                  tacky1=list(df3.ACO_ID)
                  dftacky1=list()
                  st.subheader("Inpatient Utilization in ACO")

                  fig,ax = plt.subplots(1,1)
                  for j in range(len(tacky1)):
                  #    print(df_sav.loc[(df_sav['ACO_ID'] == tacky1[j])])
                      dftacky1.append(df_sav.loc[(df_sav['ACO_ID'] == tacky1[j])])
                      dftacky1[j]= dftacky1[j].sort_values(by=['year'])
                      ax.set_title("ACO Hospital Utilization")
                      ax.set_xlabel('Year')
                      ax.set_ylabel('Number of admissions per 1000 members')
                      plt.plot(dftacky1[j].year.astype(int), dftacky1[j].ADM_S_Trm,  linewidth=3)
                      if tacky1[j]==val3:
                          plt.plot(dftacky1[j].year.astype(int), dftacky1[j].ADM_S_Trm,  color='black', marker = 'x',  label=ACO_head)
                  #        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.2)
                      ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                      ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                      plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.2)
                  plt.show()
                  st.pyplot(fig)


                  st.subheader("ACO Readmission Rate")
                  st.caption(f"Orange line indicates ACO ID: {val3}")

                  df3.Measure_479=df3.Measure_479*100
                  Measure_479_int=df3.loc[df3['ACO_ID']==val3,'Measure_479'].values[0]
                  fig,ax = plt.subplots(1,1)
                  (n, bins, patches) = ax.hist(df3.Measure_479, bins=5, label='hst',edgecolor='black', linewidth=0.5)
                  x1, y1 = [Measure_479_int, Measure_479_int], [0,  max(n)+1]
                  ax.set_title("Readmission Rate(%) for ACO members ")
                  ax.set_xlabel('Risk-standardized Readmission Rate(%) for admitted ACO members')
                  ax.set_ylabel('No. of ACOs in comparison group')
                  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                  plt.plot(x1, y1, marker = 'o')
                  plt.show()
                  st.pyplot(fig)
                  st.write("Risk-adjusted percentage of ACO assigned beneficiaries who were hospitalized and readmitted (inpatient status only, not observation) to a hospital within 30 days of discharge from the index hospital admission. A lower performance rate is indicative of better quality.")
                  st.write("No trend analysis is available for Readmission Rate.")


                  st.subheader("All-Cause Unplanned Admissions for Patients with Multiple Chronic Conditions")
                  st.caption(f"Orange line indicates ACO ID: {val3}")

                  Measure_MCC1_int=int(df3.loc[df3['ACO_ID']==val3,'Measure_MCC1'].values[0])
                  fig,ax = plt.subplots(1,1)
                  (n, bins, patches) = ax.hist(df3.Measure_MCC1, bins=5, label='hst',edgecolor='black', linewidth=0.5)
                  x1, y1 = [Measure_MCC1_int, Measure_MCC1_int], [0,  max(n)+1]
                  ax.set_title("Admissions for ACO members with Multiple Chronic Conditions for ACO members ")
                  ax.set_xlabel('All-Cause risk-standardized Unplanned Admissions for ACO members')
                  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                  ax.set_ylabel('No. of ACOs in comparison group')
                  plt.plot(x1, y1, marker = 'o')
                  plt.show()
                  st.pyplot(fig)
                  st.write("No trend analysis is available for Unplanned Admissions for Patients with Multiple Chronic Conditions.")


                  st.subheader("SNF Utilization in ACO")
                  st.caption(f"Orange line indicates ACO ID: {val3}")

                  P_SNF_ADM_int=int(df3.loc[df3['ACO_ID']==val3,'P_SNF_ADM'].values[0])
                  fig,ax = plt.subplots(1,1)
                  (n, bins, patches) = ax.hist(df3.P_SNF_ADM, bins=5, label='hst',edgecolor='black', linewidth=0.5)
                  x1, y1 = [P_SNF_ADM_int, P_SNF_ADM_int], [0,  max(n)+1]
                  #ax.hist(df3.P_SNF_ADM, bins = 5 ,edgecolor='black', linewidth=0.5)
                  ax.set_title("ACO SNF Utilization")
                  ax.set_xlabel('Number of SNF admissions per 1000 members')
                  ax.set_ylabel('No. of ACOs in comparison group')
                  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                  plt.plot(x1, y1, marker = 'o')
                  plt.show()
                  st.pyplot(fig)


                  st.subheader("SNF LOS in ACO")
                  st.caption(f"Orange line indicates ACO ID: {val3}")

                  SNF_LOS_int=int(df3.loc[df3['ACO_ID']==val3,'SNF_LOS'].values[0])
                  fig,ax = plt.subplots(1,1)
                  (n, bins, patches) = ax.hist(df3.SNF_LOS, bins=5, label='hst',edgecolor='black', linewidth=0.5)
                  x1, y1 = [SNF_LOS_int,SNF_LOS_int], [0,  max(n)+1]
                  #ax.hist(df3.SNF_LOS, bins = 5)
                  ax.set_title("ACO SNF Utilization")
                  ax.set_xlabel('SNF LoS(days) for ACO members admitted to SNF')
                  ax.set_ylabel('No. of ACOs in comparison group')
                  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                  plt.plot(x1, y1, marker = 'o')
                  plt.show()
                  st.pyplot(fig)

                  st.subheader("SNF expenses in ACO")
                  st.caption(f"Please mind that the data covers launch of PDPM (Oct '19) and PHE")
                  df_sav=dfmerge[['ACO_Name','year','CapAnn_SNF','ACO_ID']]
                  df_sav.CapAnn_SNF =df_sav.CapAnn_SNF.apply(pd.to_numeric, errors='coerce')
                  mat=list(df3.ACO_ID)
                  tacky1=list(df3.ACO_ID)
                  dftacky1=list()

                  fig,ax = plt.subplots(1,1)
                  for j in range(len(tacky1)):
                  #    print(df_sav.loc[(df_sav['ACO_ID'] == tacky1[j])])
                      dftacky1.append(df_sav.loc[(df_sav['ACO_ID'] == tacky1[j])])
                      dftacky1[j]= dftacky1[j].sort_values(by=['year'])
                      ax.set_title("SNF Expenses over time")
                      ax.set_xlabel('Year')
                      ax.set_ylabel('Annualized SNF Expense($)')
                      plt.plot(dftacky1[j].year.astype(int), dftacky1[j].CapAnn_SNF,  linewidth=3)
                      if tacky1[j]==val3:
                          plt.plot(dftacky1[j].year.astype(int), dftacky1[j].CapAnn_SNF,  color='black', marker = 'x',  label=ACO_head)
                      ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                      ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                      plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.2)
                  plt.show()
                  st.pyplot(fig)

                  st.subheader("Inpatient Rehabilitation Utilization in ACO")
                  st.caption(f"Orange line indicates ACO ID: {val3}")

                  ADM_Rehab_int=int(df3.loc[df3['ACO_ID']==val3,'ADM_Rehab'].values[0])
                  fig,ax = plt.subplots(1,1)
                  (n, bins, patches) = ax.hist(df3.ADM_Rehab, bins=5, label='hst',edgecolor='black', linewidth=0.5)
                  x1, y1 = [ADM_Rehab_int, ADM_Rehab_int], [0,  max(n)+1]
                  ax.set_title("ACO Inpatient Rehab Utilization")
                  ax.set_xlabel('Admissions to Rehab for each 1000 members')
                  ax.set_ylabel('No. of ACOs in comparison group')
                  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                  plt.plot(x1, y1, marker = 'o')
                  plt.show()
                  st.pyplot(fig)


                  st.subheader("Inpatient Rehabilitation Expenses in ACO")
                  df_sav=dfmerge[['ACO_Name','year','CapAnn_INP_Rehab','ACO_ID']]
                  df_sav.CapAnn_INP_Rehab =df_sav.CapAnn_INP_Rehab.apply(pd.to_numeric, errors='coerce')
                  mat=list(df3.ACO_ID)
                  tacky1=list(df3.ACO_ID)
                  dftacky1=list()

                  fig,ax = plt.subplots(1,1)
                  for j in range(len(tacky1)):
                  #    print(df_sav.loc[(df_sav['ACO_ID'] == tacky1[j])])
                      dftacky1.append(df_sav.loc[(df_sav['ACO_ID'] == tacky1[j])])
                      dftacky1[j]= dftacky1[j].sort_values(by=['year'])
                      ax.set_title("Inpatient Rehab Expenses over time")
                      ax.set_xlabel('Year')
                      ax.set_ylabel('Annualized Inpatient Rehab Expense($)')
                      plt.plot(dftacky1[j].year.astype(int), dftacky1[j].CapAnn_INP_Rehab,  linewidth=3)
                      if tacky1[j]==val3:
                          plt.plot(dftacky1[j].year.astype(int), dftacky1[j].CapAnn_INP_Rehab,  color='black', marker = 'x',  label=ACO_head)
                      ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                      ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                      plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.2)
                  plt.show()
                  st.pyplot(fig)

                  st.subheader("ACO Clinical Complexity (HCC-Risk Score)")
                  st.caption(f"Orange line indicates ACO ID: {val3}")

                  CMS_HCC_RiskScore_AGND_PY_int=int(df3.loc[df3['ACO_ID']==val3,'CMS_HCC_RiskScore_AGND_PY'].values[0]) 
                  fig,ax = plt.subplots(1,1)
                  (n, bins, patches) = ax.hist(df3.CMS_HCC_RiskScore_AGND_PY, bins=5, edgecolor='black', linewidth=0.5, align='left')
                  #ax.hist(df3.CMS_HCC_RiskScore_AGND_BY3, bins=5, edgecolor='black', linewidth=0.5, width=0.35)
                  x1, y1 = [CMS_HCC_RiskScore_AGND_PY_int, CMS_HCC_RiskScore_AGND_PY_int], [0,  max(n)+1]
                  ax.set_title("Population Risk distribution of ACOs")
                  ax.set_xlabel('HCC RAF of Aged-Non Dual population in ACOs')
                  ax.set_ylabel('No. of ACOs in comparison group')
                  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                  plt.plot(x1, y1, marker = 'o')
                  plt.show()
                  st.pyplot(fig)


                  #*Coding**
                  #Understand what this is saying...
                  #https://www.milliman.com/en/insight/pathways-to-success-mssp-final-rule-financial-benchmark

                  st.subheader("ACO Composite Quality Score")
                  df3=df3.drop_duplicates()
                  df3=df3.sort_values(by=['QualScore'])
                  mat=list(df3.ACO_ID)
                  clrs=[]
                  for x in mat:
                      if x != val3:
                          clrs.append('grey')
                      else:
                          clrs.append('red')
                  fig = plt.figure()
                  ax = fig.add_subplot(111)

                  x_pos = np.arange(len(df3.ACO_Name))
                  ax.set_title("ACO Quality Score")
                  ax.set_ylabel('Quality Score')
                  ax.bar(x=x_pos, height=df3.QualScore, width=0.50,align='center', color=clrs) #Colon Cancer
                  #ax.bar(x=x_pos, height=df3.QualScore, width=0.50,align='center') #Colon Cancer
                  #ax.bar(x=x_pos, height=df3.QualityID_112, width=0.35,align='center') #Breast Cancer
                  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                  plt.xticks(x_pos, df3.ACO_Name.str[0:8])
                  plt.tight_layout()
                  st.pyplot(fig)

                  df_sav=dfmerge[['ACO_Name','year','QualScore','ACO_ID']]

                  st.subheader("ACO Composite Quality Score over time")
                  mat=list(df3.ACO_ID)
                  tacky1=list(df3.ACO_ID)
                  dftacky1=list()

                  fig,ax = plt.subplots(1,1)
                  for j in range(len(tacky1)):
                  #    print(df_sav.loc[(df_sav['ACO_ID'] == tacky1[j])])
                      dftacky1.append(df_sav.loc[(df_sav['ACO_ID'] == tacky1[j])])
                      dftacky1[j]= dftacky1[j].sort_values(by=['year'])
                      ax.set_title("ACO Quality")
                      ax.set_xlabel('Year')
                      ax.set_ylabel('ACO Quality Score ')
                      plt.plot(dftacky1[j].year.astype(int), dftacky1[j].QualScore,  linewidth=3)
                      if tacky1[j]==val3:
                          plt.plot(dftacky1[j].year.astype(int), dftacky1[j].QualScore,  color='black', marker = 'x',  label=ACO_head)
                      ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                      ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                      plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.2)
                  plt.show()
                  st.pyplot(fig)



                  df3.hba1cc=100-df3.QualityID_001_WI
                  df3.hba1cc.astype(int)

                  df3['QualityID_113'].astype(float)
                  df3['QualityID_112'].astype(float)

                  st.subheader("Colon Cancer Screening")
                  mat=list(df3.ACO_ID)
                  df3=df3.sort_values(by=['QualityID_113'])

                  clrs=[]
                  for x in mat:
                      if x != val3:
                          clrs.append('grey')
                      else:
                          clrs.append('red')
                  fig = plt.figure()
                  ax = fig.add_subplot(111)
                  x_pos = np.arange(len(df3.ACO_ID))
                  ax.set_title("Appropriate screening for Colon Cancer")
                  ax.set_ylabel('Percent beneficiaries screened for Colon Cancer')
                  ax.bar(x=x_pos, height=df3.QualityID_113, width=0.50,align='center', color=clrs) #Colon Cancer
                  #ax.bar(x=x_pos, height=df3.QualityID_112, width=0.35,align='center') #Breast Cancer
                  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                  plt.xticks(x_pos, df3.ACO_Name.str[0:8])
                  plt.tight_layout()
                  st.pyplot(fig)

                  st.subheader("Colon Cancer Screening")
                  df_sav=dfmerge[['ACO_Name','year','QualityID_113','ACO_ID']]
                  df_sav.QualityID_113 =df_sav.QualityID_113.apply(pd.to_numeric, errors='coerce')
                  mat=list(df3.ACO_ID)
                  tacky1=list(df3.ACO_ID)
                  dftacky1=list()
                  fig = plt.figure()
                  fig,ax = plt.subplots(1,1)
                  for j in range(len(tacky1)):
                  #    print(df_sav.loc[(df_sav['ACO_ID'] == tacky1[j])])
                      dftacky1.append(df_sav.loc[(df_sav['ACO_ID'] == tacky1[j])])
                      dftacky1[j]= dftacky1[j].sort_values(by=['year'])
                      ax.set_title("Screening for Colon Cancer")
                      ax.set_xlabel('Year')
                      ax.set_ylabel('% Members screened for Colon Cancer')
                      plt.plot(dftacky1[j].year.astype(int), dftacky1[j].QualityID_113,  linewidth=3)
                      if tacky1[j]==val3:
                          plt.plot(dftacky1[j].year.astype(int), dftacky1[j].QualityID_113,  color='black', marker = 'x',  label=ACO_head)
                      ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                      ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                      plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.2)
                  plt.show()
                  st.pyplot(fig)


                  st.subheader("Breast Cancer Screening")

                  df3=df3.sort_values(by=['QualityID_112'])

                  mat=list(df3.ACO_ID)

                  clrs=[]
                  for x in mat:
                      if x != val3:
                          clrs.append('grey')
                      else:
                          clrs.append('red')

                  fig = plt.figure()
                  ax = fig.add_subplot(111)
                  x_pos = np.arange(len(df3.ACO_ID))
                  ax.set_title("Appropriate screening for Breast Cancer")
                  ax.set_ylabel('% Beneficiaries screened for Breast Cancer')
                  ax.bar(x=x_pos, height=df3.QualityID_112, width=0.35,align='center', color=clrs) #Breast Cancer
                  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                  plt.xticks(x_pos, df3.ACO_Name.str[0:8])
                  plt.tight_layout()
                  st.pyplot(fig)


                  st.subheader("Breast Cancer Screening")

                  df_sav=dfmerge[['ACO_Name','year','QualityID_112','ACO_ID']]
                  df_sav.QualityID_112 =df_sav.QualityID_112.apply(pd.to_numeric, errors='coerce')

                  mat=list(df3.ACO_ID)
                  tacky1=list(df3.ACO_ID)
                  dftacky1=list()

                  fig,ax = plt.subplots(1,1)
                  for j in range(len(tacky1)):
                  #    print(df_sav.loc[(df_sav['ACO_ID'] == tacky1[j])])
                      dftacky1.append(df_sav.loc[(df_sav['ACO_ID'] == tacky1[j])])
                      dftacky1[j]= dftacky1[j].sort_values(by=['year'])
                      ax.set_title("Screening for Breast Cancer")
                      ax.set_xlabel('Year')
                      ax.set_ylabel('% Members screened for Breast Cancer')
                      plt.plot(dftacky1[j].year.astype(int), dftacky1[j].QualityID_112,  linewidth=3)
                      if tacky1[j]==val3:
                          plt.plot(dftacky1[j].year.astype(int), dftacky1[j].QualityID_112,  color='black', marker = 'x',  label=ACO_head)
                      ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                      ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                      plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.2)
                  plt.show()
                  st.pyplot(fig)



                  st.subheader("Diabetes Management")
                  df3['hba1ccc']=100-(df3.QualityID_001_WI)
                  df3=df3.sort_values(by=['hba1ccc'])
                  mat=list(df3.ACO_ID)
                  clrs=[]
                  for x in mat:
                      if x != val3:
                          clrs.append('grey')
                      else:
                          clrs.append('red')
                  fig = plt.figure()
                  ax = fig.add_subplot(111)
                  x_pos = np.arange(len(df3.ACO_Name))
                  ax.set_title("Appropriate management of Diabetes (Hemoglobin A1c < 9.0%)")
                  ax.set_ylabel('Percent diabetic beneficiaries with appropriate HbA1c')
                  ax.bar(x=x_pos, height=df3.hba1ccc, width=0.25,align='center', color=clrs) #Diabetes control (inverse is better)
                  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                  plt.xticks(x_pos, df3.ACO_Name.str[0:8])
                  plt.tight_layout()
                  st.pyplot(fig)

                  st.subheader("Home Health Expenses")

                  CapAnn_HHA_int=int(df3.loc[df3['ACO_ID']==val3,'CapAnn_HHA'].values[0]) 
                  fig = plt.figure()
                  fig,ax = plt.subplots(1,1)
                  (n, bins, patches) = ax.hist(df3.CapAnn_HHA, bins=5, edgecolor='black', linewidth=0.5, align='left')
                  #ax.hist(df3.CMS_HCC_RiskScore_AGND_BY3, bins=5, edgecolor='black', linewidth=0.5, width=0.35)
                  x1, y1 = [CapAnn_HHA_int, CapAnn_HHA_int], [0,  max(n)+1]
                  ax.set_title("Home Health Expenses")
                  ax.set_xlabel('Annualized Home Health Expense($) in ACOs')
                  ax.set_ylabel('No.of ACOs in comparison group')
                  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                  plt.plot(x1, y1, marker = 'o')
                  plt.show()
                  st.pyplot(fig)
                  st.write('Home Health admissions are not available in CMS reports.')

                  st.subheader("Home Health Expenses")
                  df_sav=dfmerge[['ACO_Name','year','CapAnn_HHA','ACO_ID']]
                  df_sav.CapAnn_HHA =df_sav.CapAnn_HHA.apply(pd.to_numeric, errors='coerce')
                  mat=list(df3.ACO_ID)
                  tacky1=list(df3.ACO_ID)
                  dftacky1=list()

                  fig,ax = plt.subplots(1,1)
                  for j in range(len(tacky1)):
                  #    print(df_sav.loc[(df_sav['ACO_ID'] == tacky1[j])])
                      dftacky1.append(df_sav.loc[(df_sav['ACO_ID'] == tacky1[j])])
                      dftacky1[j]= dftacky1[j].sort_values(by=['year'])
                      ax.set_title("Home Health Expenses over time")
                      ax.set_xlabel('Year')
                      ax.set_ylabel('Annualized Home Health Expense($) per beneficiary')
                      plt.plot(dftacky1[j].year.astype(int), dftacky1[j].CapAnn_HHA,  linewidth=3)
                      if tacky1[j]==val3:
                          plt.plot(dftacky1[j].year.astype(int), dftacky1[j].CapAnn_HHA,  color='black', marker = 'x',  label=ACO_head)
                      ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                      ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                      plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.2)
                  plt.show()
                  st.pyplot(fig)

                  st.subheader("Hospice Expenses")
                  df3['CapAnn_HSP']=df3['CapAnn_HSP'].str.replace(",","")
                  df3['CapAnn_HSP']= pd.to_numeric(df3['CapAnn_HSP'])

                  fig = plt.figure()
                  fig,ax = plt.subplots(1,1)
                  CapAnn_HSP_int=int(df3.loc[df3['ACO_ID']==val3,'CapAnn_HSP'].values[0]) 
                  (n, bins, patches) = ax.hist(df3.CapAnn_HSP, bins=5, edgecolor='black', linewidth=0.5, align='left')
                  x1, y1 = [CapAnn_HSP_int, CapAnn_HSP_int], [0,  max(n)+1]
                  ax.set_title("Hospice expenses")
                  ax.set_xlabel('Annualized Hospice Expense($) per beneficiary')
                  ax.set_ylabel('No. of ACOs in comparison group')
                  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                  plt.plot(x1, y1, marker = 'o')
                  plt.show()
                  st.pyplot(fig)

                  st.subheader("Hospice Expenses")

                  df_sav=dfmerge[['ACO_Name','year','CapAnn_HSP','ACO_ID']]
                  df_sav.CapAnn_HSP =df_sav.CapAnn_HSP.apply(pd.to_numeric, errors='coerce')

                  mat=list(df3.ACO_ID)
                  tacky1=list(df3.ACO_ID)
                  dftacky1=list()

                  fig,ax = plt.subplots(1,1)
                  for j in range(len(tacky1)):
                  #    print(df_sav.loc[(df_sav['ACO_ID'] == tacky1[j])])
                      dftacky1.append(df_sav.loc[(df_sav['ACO_ID'] == tacky1[j])])
                      dftacky1[j]= dftacky1[j].sort_values(by=['year'])
                      ax.set_title("Hospice Expenses")
                      ax.set_xlabel('Year')
                      ax.set_ylabel('Annualized Hospice Expense($) per beneficiary')
                      plt.plot(dftacky1[j].year.astype(int), dftacky1[j].CapAnn_HSP,  linewidth=3)
                      if tacky1[j]==val3:
                          plt.plot(dftacky1[j].year.astype(int), dftacky1[j].CapAnn_HSP,  color='black', marker = 'x',  label=ACO_head)
                      ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                      ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                      plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.2)
                  plt.show()
                  st.pyplot(fig)


                  st.subheader(f"2021 MSSP ACO Performance Statistics")
                  st.caption(f"Median PCP visits per 1000 members for all ACOs: {P_EM_PCP_Vis_med}")
                  st.caption(f"Median PCP visits per 1000 members for 'High Revenue' ACOs : {P_EM_PCP_Vis_medH}")

                  #ADK  for all the ACOs
                  st.caption(f"Median Admits per thousand members (Short Term Hospitals) for all ACOs: {ADM_S_Trm_med}")
                  st.caption(f"Mean Admits per thousand members (Short Term Hospitals) for all ACOs: {ADM_S_Trm_mean}")
                  st.caption(f"Median Admits per thousand members (Short Term Hospitals) for 'High Revenue' ACOs : {ADM_S_Trm_medH}")

                  #EDK  for all the ACOs
                  st.caption(f"Median ED visits per thousand members (including that result in admission) for all ACOs: {ED_V_med}")
                  st.caption(f"Median ED visits per thousand members (including that result in admission)  for 'High Revenue' ACOs : {ED_V_medH}")


                  #SNF ADK  for hospital ACOs
                  st.caption(f"Median Admits per thousand members (Skilled Nursing Facilities) for all ACOs: {P_SNF_ADM_med}")
                  st.caption(f"Median Admits per thousand members (Skilled Nursing Facilities) for 'High Revenue' ACOs : {P_SNF_ADM_medH}")

                  st.caption(f"Median Length of Stay for members in Skilled Nursing Facilities for all ACOs: {SNF_LOS_med}")
                  st.caption(f"Median Length of Stay for members (Skilled Nursing Facilities) for 'High Revenue' ACOs : {SNF_LOS_medH}")

                  #Rehab Hospital LOS  for hospital ACOs
                  st.caption(f"Median Admits per thousand members (Inpatient Rehabilitation) for all ACOs: {ADM_Rehab_med}")

                  #Readmissions
                  st.caption(f"Median Readmission Rate for all ACOs: {Measure_479_med}%")
                  st.caption(f"Median Readmission Rate for all 'High Revenue' ACOs: {Measure_479_medH}%")

                  #admissions of complex patients
                  st.caption(f"Median Admission per 1000 complex members for all ACOs: {Measure_MCC1_med}")
                  st.caption(f"Median Admission per 1000 complex members for all 'High Revenue' ACOs: {Measure_MCC1_medH}")


