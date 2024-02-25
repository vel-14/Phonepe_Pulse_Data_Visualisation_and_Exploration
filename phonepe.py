import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly.express as px
import json
import requests

#connection_to_mysql

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Velcharru@1406",
    database="PhonepePulse",
    auth_plugin='mysql_native_password')

cursor=mydb.cursor()

#create_aggregated_insurance_df

cursor.execute('SELECT * FROM aggregated_insurance')
df1=cursor.fetchall()
mydb.commit()

aggregated_insurance_df=pd.DataFrame(df1,columns=('states','years','quarters','transaction_type','transaction_count','transaction_amount'))

#create_aggregated_transaction_df

cursor.execute('SELECT * FROM aggregated_transaction')
df1=cursor.fetchall()
mydb.commit()

aggregated_transaction_df=pd.DataFrame(df1,columns=('states','years','quarters','transaction_type','transaction_count','transaction_amount'))

#create_aggregaed_user_df

cursor.execute('SELECT * FROM aggregated_user')
df1=cursor.fetchall()
mydb.commit()

aggregated_user_df=pd.DataFrame(df1,columns=('states','years','quarters','brands','transaction_count','percentage'))

#create_map_insurance_df

cursor.execute('SELECT * FROM map_insurance')
df1=cursor.fetchall()
mydb.commit()

map_insurance_df=pd.DataFrame(df1,columns=('states','years','quarters','districts','transaction_count','transaction_amount'))

#create_map_transaction_df

cursor.execute('SELECT * FROM map_transaction')
df1=cursor.fetchall()
mydb.commit()

map_transaction_df=pd.DataFrame(df1,columns=('states','years','quarters','districts','transaction_count','transaction_amount'))

#create_map_user_df

cursor.execute('SELECT * FROM map_user')
df1=cursor.fetchall()
mydb.commit()

map_user_df=pd.DataFrame(df1,columns=('states','years','quarters','districts','registered_users','app_opens'))

#create_top_insurance_df

cursor.execute('SELECT * FROM top_insurance')
df1=cursor.fetchall()
mydb.commit()

top_insurance_df=pd.DataFrame(df1,columns=('states','years','quarters','pincodes','transaction_count','transaction_amount'))

#create_top_transaction_df

cursor.execute('SELECT * FROM top_transaction')
df1=cursor.fetchall()
mydb.commit()

top_transaction_df=pd.DataFrame(df1,columns=('states','years','quarters','pincodes','transaction_count','transaction_amount'))

#create_top_user_df

cursor.execute('SELECT * FROM top_user')
df1=cursor.fetchall()
mydb.commit()

top_user_df=pd.DataFrame(df1,columns=('states','years','quarters','pincodes','registeredUsers'))


#creating_bar_graph_function

def trans_amt_ct_yr(df,year):

    amt_ct_y=df[df['years']==year]
    amt_ct_y.reset_index(drop=True,inplace=True)

    amt_ct_y_grp=amt_ct_y.groupby("states")[["transaction_count","transaction_amount"]].sum()
    amt_ct_y_grp.reset_index(inplace=True)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data=json.loads(response.content)

    col1,col2 = st.columns(2)

    with col1:

        fig_amount = px.bar(amt_ct_y_grp,x="states", y="transaction_amount", title= f"{year} Transaction Amount",
                            color_discrete_sequence=px.colors.sequential.Agsunset,height=700,width=700)

        st.plotly_chart(fig_amount)

        fig_india1=px.choropleth(amt_ct_y_grp,geojson=data,locations="states", featureidkey="properties.ST_NM",
                         color="transaction_amount",color_continuous_scale="Rainbow",
                         range_color=(amt_ct_y_grp["transaction_amount"].min(),amt_ct_y_grp["transaction_amount"].min()),
                         hover_name="states", title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                         height=600,width=600)
        fig_india1.update_geos(visible=False)

        st.plotly_chart(fig_india1)

    with col2:
        fig_count = px.bar(amt_ct_y_grp,x="states", y="transaction_count", title= f"{year} Transacton Count",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=700,width=700)

        st.plotly_chart(fig_count)
    
        fig_india2=px.choropleth(amt_ct_y_grp,geojson=data,locations="states", featureidkey="properties.ST_NM",
                                color="transaction_count",color_continuous_scale="Rainbow",
                                range_color=(amt_ct_y_grp["transaction_count"].min(),amt_ct_y_grp["transaction_count"].min()),
                                hover_name="states", title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india2.update_geos(visible=False)

        st.plotly_chart(fig_india2)
    return amt_ct_y


def trans_amt_ct_yr_qr(df,quarter):
    amt_ct_y=df[df['quarters']==quarter]

    amt_ct_y.reset_index(drop=True,inplace=True)

    amt_ct_y_grp=amt_ct_y.groupby("states")[["transaction_count","transaction_amount"]].sum()

    amt_ct_y_grp.reset_index(inplace=True)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data=json.loads(response.content)

    col1,col2=st.columns(2)

    with col1:

        fig_amount = px.bar(amt_ct_y_grp,x="states", y="transaction_amount", title= f"{amt_ct_y["years"].min()} Quarter {quarter} Transaction Amount",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=700,width=700)

        st.plotly_chart(fig_amount)

        fig_india1=px.choropleth(amt_ct_y_grp,geojson=data,locations="states", featureidkey="properties.ST_NM",
                            color="transaction_amount",color_continuous_scale="Rainbow",
                            range_color=(amt_ct_y_grp["transaction_amount"].min(),amt_ct_y_grp["transaction_amount"].min()),
                            hover_name="states", title=f"{amt_ct_y["years"].min()} Quarter {quarter} TRANSACTION AMOUNT",fitbounds="locations",
                            height=600,width=600)
        fig_india1.update_geos(visible=False)

        st.plotly_chart(fig_india1)

    with col2:
        fig_count = px.bar(amt_ct_y_grp,x="states", y="transaction_count", title= f"{amt_ct_y["years"].min()} Quarter {quarter} Transacton Count",
                            color_discrete_sequence=px.colors.sequential.Agsunset,height=700,width=700)

        st.plotly_chart(fig_count)
        

        fig_india2=px.choropleth(amt_ct_y_grp,geojson=data,locations="states", featureidkey="properties.ST_NM",
                                color="transaction_count",color_continuous_scale="turbo",
                                range_color=(amt_ct_y_grp["transaction_count"].min(),amt_ct_y_grp["transaction_count"].min()),
                                hover_name="states", title=f"{amt_ct_y["years"].min()} Quarter {quarter} TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india2.update_geos(visible=False)

        st.plotly_chart(fig_india2)

    return amt_ct_y


def trans_state(df,state):
    ats=df[df["states"]==state]

    ats.reset_index(drop=True,inplace=True)

    ats_grp=ats.groupby("transaction_type")[["transaction_count","transaction_amount"]].sum()

    ats_grp.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:
        fig_agg_trans1=px.bar(ats_grp,x="transaction_count",y="transaction_type",orientation="h",height=650,
                            title=f"{state.upper()} TRANSACTION TYPE AND TRANSACTION COUNT", width=600,
                            color_discrete_sequence=px.colors.sequential.Agsunset)

        st.plotly_chart(fig_agg_trans1)

    with col2:
        fig_agg_trans2=px.bar(ats_grp,x="transaction_amount",y="transaction_type",orientation="h",height=650,
                        title=f"{state.upper()} TRANSACTION TYPE AND TRANSACTION AMOUNT", width=600,
                        color_discrete_sequence=px.colors.sequential.Agsunset)
    
        st.plotly_chart(fig_agg_trans2)

def agg_user1(df,year):
    auy=df[df["years"]==year]
    auy.reset_index(drop=True,inplace=True)
    auy_grp=pd.DataFrame(auy.groupby("brands")["transaction_count"].sum())
    auy_grp.reset_index(inplace=True)

    fig=px.bar(auy_grp,x="brands",y="transaction_count", width = 900,
               color_discrete_sequence=px.colors.sequential.Cividis,height=650,
               title=f"{year} BRANDS AND TRANSACTION COUNT")
    st.plotly_chart(fig)

    return auy

def agg_user2(df,quarter):
    auy=df[df["quarters"]==quarter]
    auy.reset_index(drop=True,inplace=True)
   

    fig=px.pie(data_frame=auy,names="brands",values="transaction_count",hover_data="percentage",
                width = 900, color_discrete_sequence=px.colors.sequential.thermal,height=650,
               title=f"{auy["years"].min()} {quarter} BRANDS AND TRANSACTION COUNT",hole=0.25)
    st.plotly_chart(fig)

    return auy

def agg_user3(df,state):
    auy=df[df["states"]==state]
    auy.reset_index(drop=True,inplace=True)
    auy_grp=pd.DataFrame(auy.groupby("brands")["transaction_count"].sum())
    auy_grp.reset_index(inplace=True)

    fig=px.line(auy_grp,x="brands",y="transaction_count", width = 900, markers=True,
               color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,
               title=f"{state.upper()} BRANDS AND TRANSACTION COUNT")
    st.plotly_chart(fig)

def map_amt_ct1(df,state):
    miy= df[df["states"] == state]
    miy_grp= miy.groupby("districts")[["transaction_count","transaction_amount"]].sum()
    miy_grp.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig1= px.bar(miy_grp, x= "districts", y= "transaction_amount",
                              width=600, height=500, title= f"{miy["years"].min()} {state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig1)

    with col2:
        fig2= px.bar(miy_grp, x= "districts", y= "transaction_count",
                              width=600, height= 500, 
                              title= f"{miy["years"].min()} {state.upper()} DISTRICTS TRANSACTION COUNT",
                              color_discrete_sequence= px.colors.sequential.Mint)
        
        st.plotly_chart(fig2)

def map_amt_ct2(df,state):
    miy= df[df["states"] == state]
    miy_grp= miy.groupby("districts")[["transaction_count","transaction_amount"]].sum()
    miy_grp.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig1= px.pie(miy_grp, names= "districts", values= "transaction_amount",
                              width=600, height=500, 
                              title= f"{miy["years"].min()} QUARTER {miy["quarters"].min()} \n{state.upper()} DISTRICTS TRANSACTION COUNT",
                              hole=0.25,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig1)

    with col2:
        fig2= px.pie(miy_grp, names= "districts", values= "transaction_count",
                              width=600, height= 500, 
                              title= f"{miy["years"].min()} QUARTER {miy["quarters"].min()} \n {state.upper()} DISTRICTS TRANSACTION COUNT",
                              hole=0.25,  color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig2)

def map_user1(df, year):
    muy= df[df["years"] == year]
    muy.reset_index(drop= True, inplace= True)
    muyg= muy.groupby("states")[["registered_users", "app_opens"]].sum()
    muyg.reset_index(inplace= True)

    fig= px.line(muyg, x= "states", y= ["registered_users","app_opens"], markers= True,
                                width=1000,height=800,title= f"{year} REGISTERED USERS AND APP OPENS", color_discrete_sequence= px.colors.sequential.Viridis_r)
    st.plotly_chart(fig)

    return muy

def map_user2(df, quarter):
    muyq= df[df["quarters"] == quarter]
    muyq.reset_index(drop= True, inplace= True)
    muyqg= muyq.groupby("states")[["registered_users", "app_opens"]].sum()
    muyqg.reset_index(inplace= True)

    fig= px.line(muyqg, x= "states", y= ["registered_users","app_opens"], markers= True,
                                title= f"{df['years'].min()} QUARTER {quarter} REGISTERED USER AND APPOPENS",
                                width= 1000,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig)

    return muyq

def map_user3(df, state):
    muyqs= df[df["states"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    muyqsg= muyqs.groupby("districts")[["registered_users", "app_opens"]].sum()
    muyqsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig1= px.bar(muyqsg, x= "districts",y= "registered_users",title= f"{state.upper()} REGISTERED USER",height=800,
                                    color_discrete_sequence= px.colors.sequential.thermal)
        st.plotly_chart(fig1)

    with col2:
        fig2= px.bar(muyqsg, x= "districts", y= "app_opens", title= f"{state.upper()} APP OPENS",height=800,
                                    color_discrete_sequence= px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig2)

def top_user1(df,year):
    tuy= df[df["years"] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["states","quarters"])["registeredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig= px.bar(tuyg, x= "states", y= "registeredUsers", barmode= "group", color= "quarters",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig)

    return tuy


def top_user2(df,state):
    tuys= df[df["states"] == state]
    tuys.reset_index(drop= True, inplace= True)

    tuysg= pd.DataFrame(tuys.groupby(["states","quarters"])["registeredUsers"].sum())
    tuysg.reset_index(inplace= True)

    fig=px.bar(tuysg, x= "quarters", y= "registeredUsers",barmode= "group",
                           width=1000, height= 800,color= "registeredUsers",
                            color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig)


def ques1():
    brand= aggregated_user_df[["brands","transaction_count"]]
    brand1= brand.groupby("brands")["transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "transaction_count", names= "brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= aggregated_transaction_df[["states", "transaction_amount"]]
    lt1= lt.groupby("states")["transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "states", y= "transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    htd= map_transaction_df[["districts", "transaction_amount"]]
    htd1= htd.groupby("districts")["transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "transaction_amount", names= "districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def ques4():
    htd= map_transaction_df[["districts", "transaction_amount"]]
    htd1= htd.groupby("districts")["transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "transaction_amount", names= "districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)


def ques5():
    sa= map_user_df[["states", "app_opens"]]
    sa1= sa.groupby("states")["app_opens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "states", y= "app_opens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)


def ques6():
    sa= map_user_df[["states", "app_opens"]]
    sa1= sa.groupby("states")["app_opens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "states", y= "app_opens", title="lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= aggregated_transaction_df[["states", "transaction_count"]]
    stc1= stc.groupby("states")["transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "states", y= "transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= aggregated_transaction_df[["states", "transaction_count"]]
    stc1= stc.groupby("states")["transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "states", y= "transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= aggregated_transaction_df[["states", "transaction_amount"]]
    ht1= ht.groupby("states")["transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "states", y= "transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    dt= map_transaction_df[["districts", "transaction_amount"]]
    dt1= dt.groupby("districts")["transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "districts", y= "transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)



#streamlit_codings


st.set_page_config(layout='wide')
st.title(":violet[Phonepe Data Visualisation & Exploration]")

with st.sidebar:
    select=option_menu("Main Menu",["Phonepe Home","Data Exploration","Top Charts"])

if select=="Phonepe Home":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
        
    col3,col4= st.columns(2)
    
    with col3:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    

elif select=="Data Exploration":
    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:
        method=st.radio("Select Analysis",["Aggregated Insurance","Aggregated Transaction","Aggregated User"])

        if method =="Aggregated Insurance":

            col1,col2=st.columns(2)

            with col1:
                years = st.slider("Select Year",aggregated_insurance_df["years"].min(),aggregated_insurance_df["years"].max(),
                                aggregated_insurance_df["years"].min())
            
            acy=trans_amt_ct_yr(aggregated_insurance_df,years)

            with col1:
                 quarters = st.slider("Select Quarter",acy["quarters"].min(),acy["quarters"].max(),
                                acy["quarters"].min())
                 
            trans_amt_ct_yr_qr(acy,quarters)

        elif method== "Aggregated Transaction":
            col1,col2=st.columns(2)

            with col1:
                years = st.slider("Select Year",aggregated_transaction_df["years"].min(),aggregated_transaction_df["years"].max(),
                                aggregated_transaction_df["years"].min())
            
            acy=trans_amt_ct_yr(aggregated_transaction_df,years)

            with col1:
                 quarters = st.slider("Select Quarter",acy["quarters"].min(),acy["quarters"].max(),
                                acy["quarters"].min())
                 
            acq=trans_amt_ct_yr_qr(acy,quarters)

            with col1:
                 states = st.selectbox("Select State",acq["states"].unique())

            trans_state(acq,states)
                 


        elif method== "Aggregated User":
            col1,col2=st.columns(2)

            with col1:
                years = st.slider("Select Year",aggregated_user_df["years"].min(),aggregated_user_df["years"].max(),
                                aggregated_user_df["years"].min())
            
            au_y=agg_user1(aggregated_user_df,years)

            with col1:
                 quarters = st.slider("Select Quarter",au_y["quarters"].min(),au_y["quarters"].max(),
                                au_y["quarters"].min())
                 
            au_q=agg_user2(au_y,quarters)

            with col1:
                 states = st.selectbox("Select State",au_q["states"].unique())
            
            agg_user3(au_q,states)



    with tab2:
        method=st.radio("Select Analysis",["Map Insurance","Map Transaction","Map User"])

        if method =="Map Insurance":
            col1,col2=st.columns(2)

            with col1:
                years_mi = st.slider("Select Year",map_insurance_df["years"].min(),map_insurance_df["years"].max(),
                                map_insurance_df["years"].min(),key="yearsmi_selectbox")
            
            mi_y=trans_amt_ct_yr(map_insurance_df,years_mi)

            with col1:
                 quarters_mi = st.slider("Select Quarter",mi_y["quarters"].min(),mi_y["quarters"].max(),
                                mi_y["quarters"].min(),key="quartersmi_selectbox")
                 
            mi_yq=trans_amt_ct_yr_qr(mi_y,quarters_mi)

            with col1:
                 states_mi = st.selectbox("Select State", mi_y["states"].unique(), key="state_selectbox")
            map_amt_ct1(mi_y,states_mi)


            with col1:
                 states = st.selectbox("Select State",mi_yq["states"].unique())
            map_amt_ct2(mi_yq,states)



        elif method== "Map Transaction":
            col1,col2=st.columns(2)

            with col1:
                years_mt = st.slider("Select Year",map_transaction_df["years"].min(),map_transaction_df["years"].max(),
                                map_transaction_df["years"].min())
            
            mt_y=trans_amt_ct_yr(map_transaction_df,years_mt)

            with col1:
                 quarters_mt = st.slider("Select Quarter",mt_y["quarters"].min(),mt_y["quarters"].max(),
                                mt_y["quarters"].min(), key="quarter_selectbox")
                 
            mt_yq=trans_amt_ct_yr_qr(mt_y,quarters_mt)

            with col1:
                 states_mt1 = st.selectbox("Select State", mt_y["states"].unique(), key="statemt1_selectbox")
            map_amt_ct1(mt_y,states_mt1)


            with col1:
                 states_mt2 = st.selectbox("Select State",mt_yq["states"].unique(),key="statemt2_selectbox")
            map_amt_ct2(mt_yq,states_mt2)

        elif method== "Map User":
            col1,col2=st.columns(2)

            with col1:
                years_mu = st.slider("Select Year",map_user_df["years"].min(),map_user_df["years"].max(),
                                map_user_df["years"].min())
            
            mu_y=map_user1(map_user_df,years_mu)

            with col1:
                 quarters_mu = st.slider("Select Quarter",mu_y["quarters"].min(),mu_y["quarters"].max(),
                                mu_y["quarters"].min(),key="quartersmu_selectbox")
                 
            mu_q=map_user2(mu_y,quarters_mu)

            with col1:
                 states_mu = st.selectbox("Select State",mu_q["states"].unique(),key="statesmu_selectbox")
            map_user3(mu_q,states_mu)
            
        


    with tab3:
        method=st.radio("Select Analysis",["Top Insurance","Top Transaction","Top User"])

        if method =="Top Insurance":
            col1,col2=st.columns(2)

            with col1:
                years_ti = st.slider("Select Year",top_insurance_df["years"].min(),top_insurance_df["years"].max(),
                                top_insurance_df["years"].min(),key="yearsti_selectbox")
            
            ti_y=trans_amt_ct_yr(top_insurance_df,years_ti)

            with col1:
                 quarters_ti = st.slider("Select Quarter",ti_y["quarters"].min(),ti_y["quarters"].max(),
                                ti_y["quarters"].min(),key="quartersti_selectbox")
                 
            trans_amt_ct_yr_qr(ti_y,quarters_ti)


        elif method== "Top Transaction":
            col1,col2=st.columns(2)

            with col1:
                years_tt = st.slider("Select Year",top_transaction_df["years"].min(),top_transaction_df["years"].max(),
                                top_transaction_df["years"].min(),key="yearstt_selectbox")
            
            tt_y=trans_amt_ct_yr(top_transaction_df,years_tt)

            with col1:
                 quarters_tt = st.slider("Select Quarter",tt_y["quarters"].min(),tt_y["quarters"].max(),
                                tt_y["quarters"].min(),key="quarterstt_selectbox")
                 
            trans_amt_ct_yr_qr(tt_y,quarters_tt)

        elif method== "Top User":
            col1,col2=st.columns(2)

            with col1:
                years_tu = st.slider("Select Year",top_user_df["years"].min(),top_user_df["years"].max(),
                                top_user_df["years"].min(),key="yearstt_selectbox")
            
            tt_y=top_user1(top_user_df,years_tu)

            with col1:
                 quarters_tu = st.slider("Select Quarter",tt_y["quarters"].min(),tt_y["quarters"].max(),
                                tt_y["quarters"].min(),key="quarterstt_selectbox")
                 
            top_user2(tt_y,quarters_tu)

elif select == "Top Charts":
    ques= st.selectbox("**Select the Question**",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
    
    if ques=="Top Brands Of Mobiles Used":
        ques1()

    elif ques=="States With Lowest Trasaction Amount":
        ques2()

    elif ques=="Districts With Highest Transaction Amount":
        ques3()

    elif ques=="Top 10 Districts With Lowest Transaction Amount":
        ques4()

    elif ques=="Top 10 States With AppOpens":
        ques5()
    
    elif ques=="Least 10 States With AppOpens":
        ques6()

    elif ques=="States With Lowest Trasaction Count":
        ques7()

    elif ques=="States With Highest Trasaction Count":
        ques8()

    elif ques=="States With Highest Trasaction Amount":
        ques9()

    elif ques=="Top 50 Districts With Lowest Transaction Amount":
        ques10()

        

