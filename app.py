import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout ='wide')

df = pd.read_csv('/Users/yuvrajdhamija/Desktop/Streamlit/Indian Startup Funding app/preprocessed_startup_funding.csv')


# data cleaning
df['investors'] = df['investors'].fillna('Undiclosed')

# lets crete that new colum for months
df['Date'] = pd.to_datetime(df['Date'])
df['year'] = df['Date'].dt.year
df['month'] = df['Date'].dt.month


def display_investor(investor):
    st.title(investor)
    # this below line will help us print the top recent investments made by this investor
    st.subheader(f'The Most Recent Investments Made by {investor}')
    st.dataframe(df[df['investors'].str.contains(investor)].head())
    
    # now we also write the code to show the bigest investments by the particular seleceted investor
    col1 , col2 = st.columns(2)

    with col1:

    
        a_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending = False).head()
        st.subheader('Top Investments')

        fig , ax = plt.subplots()
        ax.bar(a_series.index , a_series.values)
        st.pyplot(fig)

    with col2:
        # we are gonna print the pie chart in this side
        v_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        st.subheader('Sectors invested in')

        fig1 , ax1 = plt.subplots()
        ax1.pie(v_series , labels = v_series.index)
        st.pyplot(fig1)

    
    col3 , col4 = st.columns(2)

    with col3:
        r_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()

        st.subheader('Investments made round wise')

        fig3, ax3 = plt.subplots()
        ax3.pie(r_series , labels = r_series.index)
        st.pyplot(fig3)

    with col4:
        c_series = df[df['investors'].str.contains(investor)].groupby('City  Location')['amount'].sum()
        st.subheader('City wise Investment data')

        fig4 , ax4 = plt.subplots()

        ax4.pie(c_series , labels = c_series.index)
        st.pyplot(fig4)


    # now we have to create a YoY line chart for each investor which shows total investment made per year by an investor
    # sabse pehle to year ki info nikaal ke well create a new column
    
    # hahaha same thing happened with sir also , the date time obj automat got converted back to o tyype

    y_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    fig5, ax5 = plt.subplots()

    ax5.plot(y_series.index , y_series.values)
    st.pyplot(fig5)




def display_general():
    col1 , col2 , col3 , col4 = st.columns(4)

    total = round(df['amount'].sum())
    # this rn prints the entire series ki row 
    # max_fund = round(df.groupby('startup')['amount'].max().sort_values(ascending = False))

    max_fund = round(df.groupby('startup')['amount'].max().sort_values(ascending = False).head(1).values[0])

    # now how will we find the avg money invested in startups
    avg_fund = round(df.groupby('startup')['amount'].sum().mean())

    # now lets us also show the no of funded startups , we find the unique values only as a startu might appear mtultpile times
    s_count = len(df['startup'].unique())

    # we couldve also found out about the no of startups using the nunique wala method

    with col1:
        st.metric('Total' , str(total) + 'Cr')

    with col2:
        # in this we wil print the max funding made till now , also consider the fat that a compay might bag funding at multiple rounds
        st.metric('Max' , str(max_fund) + 'Cr')
    
    with col3:
        st.metric('Avg' , str(avg_fund) + 'Cr')
    
    with col4:
        st.metric('Funded Startups' , str(s_count))


        # now issi genreal wale analysid mei we would show a graph of MoM investments . basiccally per month jo investments 
        # ho rahi hongi 
    # x = df.groupby(['year' , 'month'])['amount'].sum().reset_index()
   

    # now iss x wale df ka we can create a graph jaha pe y axis would be x[amount] and 
    x = df.groupby(['year' , 'month'])
    
        
   
    
    choose  =st.selectbox('Select the basis on which you want the graph' , ['Count' , 'Total Amount'])

    if choose == 'Count':
        x = x['amount'].count().reset_index()
        st.subheader('No of investments per month')
        # st.pyplot(fig5)
    else:
        x = x['amount'].sum().reset_index()
        
        st.subheader('Total amount of investments made per month')
        # st.pyplot(fig

    x['year_month'] =(
        x['year'].astype(str) + '-' + x['month'].astype(str).str.zfill(2)
    )

    fig5 , ax5 = plt.subplots()
    ax5.plot(x['year_month'] , x['amount'])

    

    




    
    st.pyplot(fig5)

# st.dataframe(df)



st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select an Option' , ['Overall Analysis' , 'StartUp' , 'Investor'])

if option=='Overall Analysis':
    st.title('Overall Analysis')
    but0 = st.sidebar.button('Show overall')
    
    if but0:
        display_general()
elif option =='StartUp':
    st.sidebar.selectbox('Select Startup' ,  sorted(df['startup'].unique()))
    bt1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
else:
    invst =st.sidebar.selectbox('Select Investor' , sorted(set(df['investors'].str.split(',').sum())))
    bt2 = st.sidebar.button('Find Investor Details')
    if bt2:
    
        # here wwe are going to call the function which will print the name of the investor and their last 
        # 5 investments made 
        # this function will only be called when the user presses that button
        display_investor(invst)

        






