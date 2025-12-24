import streamlit as st
import pandas as pd

email = st.text_input('Enter your email')

password = st.text_input('Enter your password')

button = st.button('Login')

if button:
    # this is is piece of code which will run when the button is clicked
    if email =='yuvrajdhamija02@gmail.com' and password == '123':
        st.success('Thank you for logging in')
        st.balloons()
    else:
        st.error('wrong password')


# NOW HOW TO MAKE A DROPDOWN LIST FOR YOUR USER TO SELEVT SOME INPUT
gender = st.selectbox('Select Your Section' , ['A' , 'B' , 'C' , 'D'])

#HOW TO TAKE INPUT FROM THE USER
file = st.file_uploader('Upload a CSV file')

if file is not None:
    df = pd.read_csv(file)
    st.dataframe(df.describe())

