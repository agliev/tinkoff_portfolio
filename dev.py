#!/usr/bin/env python
# coding: utf-8

# In[8]:


import tinvest 
from secrets import TOKEN
import pandas as pd
pd.options.display.float_format = '{:,}'.format
 


# In[18]:


EX_RATE_DICT = {"usd":71.5, "rub":1}
client = tinvest.SyncClient(TOKEN)


# In[16]:


def export_portfolio(client):
    df = pd.DataFrame(client.get_portfolio().dict()['payload']["positions"])
    df["currency"] = df["average_position_price"].map(lambda i: i["currency"])
    df["average_position_price"] = df["average_position_price"].map(lambda i: i["value"])
    df["currency"] = df["currency"].map(lambda i: i.name)
    df["expected_yield"] = df["expected_yield"].map(lambda i: i["value"])
    df["instrument_type"] = df["instrument_type"].map(lambda i: i.name)
    df["currency_mult"] = df["currency"].replace(EX_RATE_DICT)
    df["rub_position_price"] = df["average_position_price"].map(float)*df["currency_mult"]
    df["rub_expected_yield"] = df["expected_yield"].map(float)*df["currency_mult"]
    df["total_position_price"] = df["rub_position_price"]*df["balance"].map(float)
    df["average_position_price"] = df["average_position_price"].apply(lambda x: f"{x:.2f}".replace('.', ','))
    df["balance"] = df["balance"].apply(lambda x: f"{x:.2f}".replace('.', ','))
    df["expected_yield"] = df["expected_yield"].apply(lambda x: f"{x:.2f}".replace('.', ','))
    
    return df


# In[21]:


df = export_portfolio(client)


# In[22]:


df.to_excel("Table.xlsx", float_format="%.2f")

