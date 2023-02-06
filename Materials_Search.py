#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime as dt


# In[18]:


excel = pd.read_excel('material inventory tracking log cp 24feb21.xlsx', index_col='Client')
temp = pd.DataFrame(excel)
temp.head()


# In[19]:


tests = temp[' Expiration/Re-test'].astype(str)
dates = []
for test in tests:
    dates.append(test[:-9])

temp[' Expiration/Re-test']= dates

temp.head()


# In[20]:


tests = temp['Checkout Date'].astype(str)
dates = []
for test in tests:
    dates.append(test[:-9])

temp['Checkout Date']= dates

temp.head()


# In[24]:


temp.dropna(subset=['Balance'], inplace=True)
temp.head()


# In[26]:


temp = temp.loc[:,['Recd', 'Item/Product #', 'Material Description', 'Vendor', 'Manufacturer', 'LPI-Batch', 'Batch', ' Expiration/Re-test', 'Initial Balance', 'UOM', 'Balance']]
temp.head()


# In[27]:


temp.to_csv('Materials Database.csv')


# In[28]:


file = 'Materials Database.csv'
data = pd.read_csv(file, index_col=False)
df = pd.DataFrame(data)

st.title('Materials Database')


# In[ ]:


@st.cache
def load_data():
    df = pd.read_csv('Materials Database.csv')
    return df

df = load_data()


# In[ ]:


def search(df, column, search_term):
    if column == 'Material Name':
        search_term = (search_term)
        
    indexes = df.loc[df[column].isin([search_term])].index
    if indexes.size > 0:
        return df.iloc[indexes]
    else:
        return[]


# In[ ]:


buffer, col2, col3 = st.columns([1, 20, 40])

with col2:
    key = st.selectbox("Key",['Client','Item/Product #','Material Name', 'Vendor', 'Manufacturer', 'LPI-Lot Number', 'Initial Balance', 'Removed Qty', 'Returned Qty', 'Balance', 'Checkout Date'])

with col3:
    search_term = st.text_input("Search")
    if key != '' and search_term != '':
        df = search(data, key, search_term)

buffer, col2 = st.columns([1, 100])

with col2:
    if not df.empty:
        st.dataframe(df)
    else:
        st.write('Did not find any matching criteria')

