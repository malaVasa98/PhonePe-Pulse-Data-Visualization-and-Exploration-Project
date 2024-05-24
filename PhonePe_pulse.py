# Pip install streamlit, streamlit_option_menu, git clone before running the code
import streamlit as st
from streamlit_option_menu import option_menu
import json
import pandas as pd
import os
import plotly.express as px
st.set_page_config(layout="wide")
st.title(":blue[PhonePe Pulse Data Visualization and Exploration]")
with st.sidebar:
    selected = option_menu('Menu',["About","Table details","Data Visualization and Exploration"])
if selected=="About":
    st.write("In this project, we consider the PhonePe Pulse data that is available in a Github repository and clone the Github repository in Python and access the files and construct each table of Aggregated Transaction, Aggregated User, Map Transaction, Map User, Top Transaction (District), Top Transaction (PINCODE), Top User (District) and Top User (PINCODE). Her we consider each state / union territory of India and consider the details from 2018-2024 (available in four quarters). We perform Data Analysis and display it through geo-visualisation and other data visualisation formats like Bar Plot, Pie Chart, etc., to get observations and meaningful insights.")
if selected=="Table details":
    tab1,tab2,tab3=st.tabs(["Aggregated","Map","Top"])
    with tab1:
        agg_sel = st.radio("Aggregated",["Transaction","User"])
        if agg_sel == "Transaction":
            df_agg_trans = pd.read_csv('Aggregated_Transaction.csv')
            st.dataframe(df_agg_trans)
        elif agg_sel == "User":
            df_agg_user = pd.read_csv("Aggregated_User.csv")
            st.dataframe(df_agg_user)
    with tab2:
        map_sel = st.radio("Map",["Transaction","User"])
        if map_sel=="Transaction":
            df_map_trans = pd.read_csv('Map_transaction.csv')
            st.dataframe(df_map_trans)
        elif map_sel=="User":
            df_map_user = pd.read_csv('Map_user.csv')
            st.dataframe(df_map_user)
    with tab3:
        top_sel = st.radio("Top",["Transaction","User"])
        if top_sel=="Transaction":
            opt = st.selectbox("Select one",('District','PINCODE'),index=False)
            if opt=='District':
                df_top_trans_dis = pd.read_csv('Top_transaction_dis.csv')
                st.dataframe(df_top_trans_dis)
            elif opt=='PINCODE':
                df_top_trans_pin = pd.read_csv('Top_transaction_pin.csv')
                st.dataframe(df_top_trans_pin)
        elif top_sel=='User':
            opt = st.selectbox("Select one",('District','PINCODE'),index=False)
            if opt=='District':
                df_top_user_dis = pd.read_csv('Top_user_dis.csv')
                st.dataframe(df_top_user_dis)
            elif opt=='PINCODE':
                df_top_user_pin = pd.read_csv('Top_user_pin.csv')
                st.dataframe(df_top_user_pin)
# SQL Table
from sqlalchemy import create_engine
engine = create_engine('sqlite:///PhonePe_data.db')

if selected=="Data Visualization and Exploration":
    tab1,tab2,tab3,tab4=st.tabs(["Aggregated","Map","Top (District)","Top (PINCODE)"])
    qu = {
        "Q1":"What is the average transaction amount for each year and each quarter in each state?",
        "Q2":"What is the total transaction count for each transaction type, for each year in each state?",
        "Q3":"Which user brand name has maximum user count?"
    }
    with tab1:
        optz = st.selectbox('Select a query',tuple(qu.values()),index=False)
        if optz==qu["Q1"]:
            df_agg_trans = pd.read_csv('Aggregated_Transaction.csv')
            df_agg_trans.to_sql('Aggregated_transaction', con=engine, if_exists='replace', index=False)
            df_q1 = pd.read_sql('''select State,Year,Quarter,avg(Transaction_amount) as Average_transaction
                       from Aggregated_Transaction
                       group by State,Year,Quarter''',con=engine)
            col1,col2=st.columns(2)
            with col1:
                year_agq1 = st.slider('Select Year',df_agg_trans.Year.min(),df_agg_trans.Year.max(),key="yr_ag_s1")
            with col2:
                quarter_agq1 = st.slider('Select Quarter',df_agg_trans.Quarter.min(),df_agg_trans.Quarter.max(),key="yr_qr_s1")
            df_yr = df_q1[df_q1.Year==year_agq1]
            df_qr = df_yr[df_yr.Quarter==quarter_agq1]
            fig = px.bar(df_qr,x="State",y='Average_transaction',title=f'Average Transaction in {year_agq1} Quarter {quarter_agq1}',
                             color_discrete_sequence= px.colors.sequential.Plasma_r,height=650,width=600)
            st.plotly_chart(fig)
            fig = px.choropleth(df_qr,
                                 geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                          featureidkey='properties.ST_NM',
                          locations='State',
                          color='Average_transaction',
                          color_continuous_scale='Reds',
                          title=f'Average Transaction in {year_agq1} Quarter {quarter_agq1}'
                          )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)
        if optz==qu["Q2"]:
            df_agg_trans = pd.read_csv('Aggregated_Transaction.csv')
            df_agg_trans.to_sql('Aggregated_transaction', con=engine, if_exists='replace', index=False)
            df_q2 = pd.read_sql('''select State,Year,Transaction_type,sum(Transaction_count) as Total_Transaction_Count
                        from Aggregated_Transaction
                        group by State,Year,Transaction_type''',con=engine)
            q_key = dict(zip(list(range(1,6)),list(df_q2.Transaction_type.unique())))
            st.write(q_key)
            col1,col2 = st.columns(2)
            with col1:
                year_agq2 = st.slider('Select Year',df_agg_trans.Year.min(),df_agg_trans.Year.max(),key="yr_ag_s2")
            with col2:
                trans_type = st.slider('Select Transaction type',1,5)
            df_q22 = df_q2[df_q2.Year==year_agq2]
            df_q221 = df_q22[df_q22.Transaction_type==q_key[trans_type]]
            fig1 = px.choropleth(df_q221,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_Transaction_Count',
                    color_continuous_scale='Rainbow',
                    title=f'Total Transaction Count in {year_agq2} for {q_key[trans_type]}'
                    )
            fig1.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig1)
        if optz==qu["Q3"]:
            df_agg_user = pd.read_csv('Aggregated_User.csv')
            df_agg_user.to_sql('Aggregated_user',con=engine,if_exists='replace',index=False)
            df_q3 = pd.read_sql('''select State,Year,User_brand_name,max(User_count) as Max_count
                                   from Aggregated_user
                                   group by State,Year''',con=engine)
            col1,col2 = st.columns(2)
            with col1:
                year_agq3 = st.slider('Select Year',df_agg_user.Year.min(),df_agg_user.Year.max(),key="yr_ag_s3")
            df_q33 = df_q3[df_q3.Year==year_agq3]
            fig = px.choropleth(df_q33,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='User_brand_name',
                    color_continuous_scale='Pink',
                    title=f'Maximum User brand in {year_agq3}'
                    )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)
            df_q33.to_sql('Samp_data',con=engine,if_exists='replace',index=False)
            df_q331 = pd.read_sql('''select User_brand_name,count(User_brand_name) as count from Samp_data group by User_brand_name''',con=engine)
            dif = px.pie(df_q331,names='User_brand_name',values='count',title=f'Number of states for which the given brand has maximum count - Year {year_agq3}')
            st.plotly_chart(dif)
    qu_mp = {
                 "Q1":"In each year and quarter, which district has maximum transaction count?",
                 "Q2":"What is the sum of total transaction value for each year and quarter in each state?",
                 "Q3":"In each year and quarter, what are the total no. of Registered users and App opens?",
            }
    with tab2:
        optz_mp = st.selectbox('Select a Query',tuple(qu_mp.values()),index=False)
        if optz_mp==qu_mp["Q1"]:
            df_map_trans = pd.read_csv('Map_transaction.csv')
            df_map_trans.to_sql('Map_transaction',con=engine,if_exists='replace',index=False)
            df_mq1 = pd.read_sql('''select State,Year,Quarter,District_name,max(Transaction_count_district) as Max_trans_count
                        from Map_transaction
                        group by State,Year,Quarter''',con=engine)
            col1,col2=st.columns(2)
            with col1:
                year_mpq1 = st.slider("Select Year",df_map_trans.Year.min(),df_map_trans.Year.max(),key="yr_mp_s1")
            with col2:
                quarter_mpq1 = st.slider("Select Quarter",df_map_trans.Quarter.min(),df_map_trans.Quarter.max(),key="qr_mp_s1")
            df_mq11 = df_mq1[df_mq1.Year==year_mpq1]
            df_mq111 = df_mq11[df_mq11.Quarter==quarter_mpq1]
            fig = px.choropleth(df_mq111,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Max_trans_count',
                    color_continuous_scale='Rainbow',
                    hover_data={'District_name': True},
                    title=f'Maximum Transaction Count in {year_mpq1} Quarter {quarter_mpq1}'
                    )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)
            df_mq111.to_sql('District_tab',con=engine,if_exists='replace',index=False)
            df_mq1_ds = pd.read_sql('''select State,District_name,Max_trans_count from District_tab order by Max_trans_count desc''',con=engine)
            st.dataframe(df_mq1_ds)
        if optz_mp==qu_mp["Q2"]:
            df_map_trans = pd.read_csv('Map_transaction.csv')
            df_map_trans.to_sql('Map_transaction',con=engine,if_exists='replace',index=False)
            df_mq2 = pd.read_sql('''select State,Year,Quarter,sum(Total_transaction_value) as Total
                        from Map_transaction
                        group by State,Year,Quarter''',con=engine)
            col1,col2 = st.columns(2)
            with col1:
                year_mpq2 = st.slider('Select Year',df_map_trans.Year.min(),df_map_trans.Year.max(),key="yr_mp_s2")
            with col2:
                quarter_mpq2 = st.slider('Select Quarter',df_map_trans.Quarter.min(),df_map_trans.Quarter.max(),key="qr_mp_s2")
            
            df_mq22 = df_mq2[df_mq2.Year==year_mpq2]
            df_mq222 = df_mq22[df_mq22.Quarter==quarter_mpq2]
            fig = px.bar(df_mq222,x="State",y='Total',title=f'Sum of Total Transaction in {year_mpq2} Quarter {quarter_mpq2}',
                         color_discrete_sequence= px.colors.sequential.Inferno,height=650,width=600)
            st.plotly_chart(fig)
            fig = px.choropleth(df_mq222,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total',
                    color_continuous_scale='Reds',
                    title=f'Sum of Total Transaction in {year_mpq2} Quarter {quarter_mpq2}'
                    )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)
            
        if optz_mp==qu_mp["Q3"]:
            df_map_user = pd.read_csv('Map_user.csv')
            df_map_user.to_sql('Map_User',con=engine,if_exists='replace',index=False)
            df_mq3 = pd.read_sql('''select State,Year,Quarter,sum(Registered_users) as Total_reg_users,sum(App_opens) as Total_app_opens
                        from Map_User
                        group by State,Year,Quarter''',con=engine)
            col1,col2 = st.columns(2)
            with col1:
                year_mpq3 = st.slider('Select Year',df_map_user.Year.min(),df_map_user.Year.max(),key="yr_mp_s3")
            with col2:
                quarter_mpq3 = st.slider('Select Quarter',df_map_user.Quarter.min(),df_map_user.Quarter.max(),key="qr_mp_s3")
            df_mq33 = df_mq3[df_mq3.Year==year_mpq3]
            df_mq333 = df_mq33[df_mq33.Quarter==quarter_mpq3]
            col1,col2 = st.columns(2)
            with col1:
                
                fig = px.bar(df_mq333,x='State',y='Total_reg_users',title=f'Total registered users in {year_mpq3} Quarter {quarter_mpq3}',
             color_discrete_sequence=px.colors.sequential.Hot,height=650,width=520)
                st.plotly_chart(fig)
            with col2:
                
                fig = px.bar(df_mq333,x='State',y='Total_app_opens',title=f'Total App opens in {year_mpq3} Quarter {quarter_mpq3}',
             color_discrete_sequence=px.colors.sequential.Plasma,height=650,width=520)
                st.plotly_chart(fig)
            
            col1,col2 = st.columns(2)
            with col1:
                
                fig = px.choropleth(df_mq333,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_reg_users',
                    color_continuous_scale='purples',
                    title=f'Total registered users in {year_mpq3} Quarter {quarter_mpq3}',height=650,width=520
                    )
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)
                
            with col2:
                
                fig = px.choropleth(df_mq333,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_app_opens',
                    color_continuous_scale='purples',
                    title=f'Total App opens in {year_mpq3} Quarter {quarter_mpq3}',height=650,width=520
                    )
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig)
    qu_to_dis = {
        "Q1":"What is the average total transaction of the top 10 districts for each year and quarter in each state?",
        "Q2":"In each state, which district has maximum transaction count for each year and quarter?",
        "Q3":"In each state, what is the sum of total registered users for each year and quarter?"
        }
    with tab3:
        optz_td = st.selectbox('Select a Query',tuple(qu_to_dis.values()),index=False)
        if optz_td==qu_to_dis["Q1"]:
            df_top_trans_dis = pd.read_csv('Top_transaction_dis.csv')
            df_top_trans_dis.to_sql('Top_transaction_dis',con=engine,if_exists='replace',index=False)
            df_ttdq1 = pd.read_sql('''select State,Year,Quarter,avg(Total_transaction_top_dis) as Average
                          from Top_transaction_dis
                          group by State,Year,Quarter''',con=engine)
            col1,col2 = st.columns(2)
            with col1:
                year_tdq1 = st.slider('Select Year',df_top_trans_dis.Year.min(),df_top_trans_dis.Year.max(),key="yr_td_s1")
            with col2:
                quarter_tdq1 = st.slider('Select Quarter',df_top_trans_dis.Quarter.min(),df_top_trans_dis.Quarter.max(),key="qr_td_s1")
            df_ttdq11 = df_ttdq1[df_ttdq1.Year==year_tdq1]
            df_ttdq111 = df_ttdq11[df_ttdq11.Quarter==quarter_tdq1]
            fig = px.bar(df_ttdq111,x='State',y='Average',title=f'Average total transaction in {year_tdq1} Quarter {quarter_tdq1}',
             color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
            st.plotly_chart(fig)
            fig = px.choropleth(df_ttdq111,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Average',
                    color_continuous_scale='delta',
                    title=f'Average total transaction in {year_tdq1} Quarter {quarter_tdq1}'
                    )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)
        if optz_td==qu_to_dis["Q2"]:
            df_top_trans_dis = pd.read_csv('Top_transaction_dis.csv')
            df_top_trans_dis.to_sql('Top_transaction_dis',con=engine,if_exists='replace',index=False)
            df_ttdq2 = pd.read_sql('''select State,Year,Quarter,District_name,max(Transaction_count_top_dis) as Max
                          from Top_transaction_dis
                          group by State,Year,Quarter''',con=engine)
            col1,col2=st.columns(2)
            with col1:
                year_tdq2 = st.slider('Select Year',df_top_trans_dis.Year.min(),df_top_trans_dis.Year.max(),key="yr_td_s2")
            with col2:
                quarter_tdq2 = st.slider('Select Quarter',df_top_trans_dis.Quarter.min(),df_top_trans_dis.Quarter.max(),key="qr_td_s2")
            df_ttdq22 = df_ttdq2[df_ttdq2.Year==year_tdq2]
            df_ttdq222 = df_ttdq22[df_ttdq22.Quarter==quarter_tdq2]
            fig = px.choropleth(df_ttdq222,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Max',
                    color_continuous_scale='sunset',
                    hover_data={'District_name':True},
                    title=f'Maximum transaction count in {year_tdq2} Quarter {quarter_tdq2}'
                    )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)
            df_ttdq222.to_sql('Dis_trans',con=engine,if_exists='replace',index=False)
            df_td_ds = pd.read_sql('''select State,District_name,Max from Dis_trans order by Max desc''',con=engine)
            st.dataframe(df_td_ds)
        if optz_td==qu_to_dis["Q3"]:
            df_top_user_dis = pd.read_csv('Top_user_dis.csv')
            df_top_user_dis.to_sql('Top_user_dis',con=engine,if_exists='replace',index=False)
            df_ttdq3 = pd.read_sql('''select State,Year,Quarter,sum(Total_registered_users_dis) as Total_sum
                          from Top_user_dis
                          group by State,Year,Quarter''',con=engine)
            col1,col2=st.columns(2)
            with col1:
                year_tdq3 = st.slider('Select Year',df_top_user_dis.Year.min(),df_top_user_dis.Year.max(),key="yr_td_s3")
            with col2:
                quarter_tdq3 = st.slider('Select Quarter',df_top_user_dis.Quarter.min(),df_top_user_dis.Quarter.max(),key="qr_td_s3")
            df_ttdq33 = df_ttdq3[df_ttdq3.Year==year_tdq3]
            df_ttdq333 = df_ttdq33[df_ttdq33.Quarter==quarter_tdq3]
            fig = px.bar(df_ttdq333,x='State',y='Total_sum',title=f'Sum of total registered users in {year_tdq3} Quarter {quarter_tdq3}',
             color_discrete_sequence=px.colors.sequential.Turbo,height=650,width=600)
            st.plotly_chart(fig)
            fig = px.choropleth(df_ttdq333,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_sum',
                    color_continuous_scale='puor',
                    title=f'Sum of total registered users in {year_tdq3} Quarter {quarter_tdq3}'
                    )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)
    qu_to_pin = {
        "Q1":"What is the average total transaction of the top 10 PINCODEs for each year and quarter in each state?",
        "Q2":"In each state, which PINCODE has maximum transaction count for each year and quarter?",
        "Q3":"In each state, what is the sum of total registered users for each year and quarter?"
        }
    with tab4:
        optz_tp = st.selectbox('Select a query',tuple(qu_to_pin.values()),index=False)
        if optz_tp==qu_to_pin["Q1"]:
            df_top_trans_pin = pd.read_csv('Top_transaction_pin.csv')
            df_top_trans_pin.to_sql('Top_transaction_pin',con=engine,if_exists='replace',index=False)
            df_ttpq1 = pd.read_sql('''select State,Year,Quarter,avg(Total_transaction_top_pin) as Average_total_transaction
                          from Top_transaction_pin
                          group by State,Year,Quarter''',con=engine)
            col1,col2=st.columns(2)
            with col1:
                year_tpq1 = st.slider('Select Year',df_top_trans_pin.Year.min(),df_top_trans_pin.Year.max(),key="yr_tp_s1")
            with col2:
                quarter_tpq1 = st.slider('Select Quarter',df_top_trans_pin.Quarter.min(),df_top_trans_pin.Quarter.max(),key="qr_tp_s1")
            df_ttpq11 = df_ttpq1[df_ttpq1.Year==year_tpq1]
            df_ttpq111 = df_ttpq11[df_ttpq11.Quarter==quarter_tpq1]
            fig = px.bar(df_ttpq111,x='State',y='Average_total_transaction',title=f'Average total transaction in {year_tpq1} Quarter {quarter_tpq1}',
             color_discrete_sequence=px.colors.sequential.Viridis,height=650,width=600)
            st.plotly_chart(fig)
            fig = px.choropleth(df_ttpq111,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Average_total_transaction',
                    color_continuous_scale='algae',
                    title=f'Average total transaction in {year_tpq1} Quarter {quarter_tpq1}'
                    )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)
        if optz_tp==qu_to_pin["Q2"]:
            df_top_trans_pin = pd.read_csv('Top_transaction_pin.csv')
            df_top_trans_pin.to_sql('Top_transaction_pin',con=engine,if_exists='replace',index=False)
            df_ttpq2 = pd.read_sql('''select State,Year,Quarter,cast(PINCODE as int) as PINCODE,max(Transaction_count_top_pin) as Maximum_Transaction_Count
                          from Top_transaction_pin
                          group by State,Year,Quarter''',con=engine)
            col1,col2=st.columns(2)
            with col1:
                year_tpq2=st.slider('Select Year',df_top_trans_pin.Year.min(),df_top_trans_pin.Year.max(),key="yr_tp_s2")
            with col2:
                quarter_tpq2=st.slider('Select Quarter',df_top_trans_pin.Quarter.min(),df_top_trans_pin.Quarter.max(),key="qr_tp_s2")
            df_ttpq22 = df_ttpq2[df_ttpq2.Year==year_tpq2]
            df_ttpq222 = df_ttpq22[df_ttpq22.Quarter==quarter_tpq2]
            fig = px.choropleth(df_ttpq222,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Maximum_Transaction_Count',
                    color_continuous_scale='thermal',
                    hover_data={'PINCODE':True},
                    title=f'Maximum transaction count in {year_tpq2} Quarter {quarter_tpq2}'
                    )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)
            df_ttpq222.to_sql('Top_trans_pin',con=engine,if_exists='replace',index=False)
            df_tp_ds = pd.read_sql('''select State,PINCODE,Maximum_Transaction_Count from Top_trans_pin order by Maximum_transaction_count desc''',con=engine)
            st.dataframe(df_tp_ds)
        if optz_tp==qu_to_pin["Q3"]:
            df_top_user_pin = pd.read_csv('Top_user_pin.csv')
            df_top_user_pin.to_sql('Top_user_pin',con=engine,if_exists='replace',index=False)
            df_ttpq3 = pd.read_sql('''select State,Year,Quarter,sum(Total_registered_users_pin) as Total_Sum
                          from Top_user_pin
                          group by State,Year,Quarter''',con=engine)
            col1,col2=st.columns(2)
            with col1:
                year_tpq3=st.slider('Select Year',df_top_user_pin.Year.min(),df_top_user_pin.Year.max(),key="yr_tp_s3")
            with col2:
                quarter_tpq3=st.slider('Select Quarter',df_top_user_pin.Quarter.min(),df_top_user_pin.Quarter.max(),key="qr_tp_s3")
            df_ttpq33 = df_ttpq3[df_ttpq3.Year==year_tpq3]
            df_ttpq333 = df_ttpq33[df_ttpq33.Quarter==quarter_tpq3]
            fig = px.bar(df_ttpq333,x='State',y='Total_Sum',title=f'Sum of total registered users in {year_tpq3} Quarter {quarter_tpq3}',
             color_discrete_sequence=px.colors.sequential.haline,height=650,width=600)
            st.plotly_chart(fig)
            fig = px.choropleth(df_ttpq333,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_Sum',
                    color_continuous_scale='hsv',
                    title=f'Sum of total registered users in {year_tpq3} Quarter {quarter_tpq3}'
                    )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)
        
             
        
                
        
        
            

            
            
    