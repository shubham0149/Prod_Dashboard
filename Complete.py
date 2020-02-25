#!/usr/bin/env python
# coding: utf-8

# # <div style="text-align: center">HROS Production Runtimes Dashboard</div>

# In[1]:


# !pip install pandas

# !pip install numpy

# !pip install ipywidgets
# jupyter nbextension enable --py widgetsnbextension

# !pip install plotly

# !pip install jupyter_dashboards
# jupyter nbextension install --py jupyter_dashboards --sys-prefix
# jupyter nbextension enable --py jupyter_dashboards --sys-prefix
# pip install termcolor


# In[2]:


import pandas as pd
import numpy as np
from ipywidgets import interact
from IPython.display import display
import plotly.graph_objects as go
import ipywidgets as widgets
import datetime
import warnings
warnings.filterwarnings("ignore")
from datetime import date, timedelta
import plotly.express as px
from plotly.subplots import make_subplots
#import chart_studio.plotly as py
from termcolor import colored,cprint

location = "C:\\Users\\Shubham.k\\Downloads\\RDP DI - Dashboard"


# In[3]:


df1 = pd.read_excel(location +'\\test_2.xlsx') # Overall level data
df2 = pd.read_excel(location + '\\test.xlsx') # daily level data


# In[4]:


df_cleaned = df1[df1['Activation']<'2020-01-23']

Last_refresh_dt = max(pd.to_datetime(df2['End']))


# In[5]:


df_cleaned['Activation'] = pd.to_datetime(df_cleaned['Activation']).dt.strftime('%d-%b-%y')
df_cleaned['Start time'] = pd.to_datetime(df_cleaned['Start time'])
df_cleaned['End'] = pd.to_datetime(df_cleaned['End'])


# In[6]:


df_cleaned.reset_index(inplace=True)


# In[7]:


def convert(seconds,flag):
    if flag == 0:
        seconds = seconds % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%02d.%02d" % (hour, minutes)
    elif flag == 1:
        return "%02d:%02d" % (hour, minutes)


# In[8]:


df_cleaned['start_time'] = df_cleaned['Start time'].dt.date
#df1['end_time'] = df1['End'].dt.date
l = list()

for i in range(len(df_cleaned)):
    s = str(df_cleaned['start_time'][i]) + " 00:00:00"
    l.append(s)

df_cleaned['start_time'] = l
df_cleaned['start_time'] = pd.to_datetime(df_cleaned['start_time'])


df_cleaned['end_time'] = df_cleaned['End'].dt.date
#df1['end_time'] = df1['End'].dt.date
l = list()

for i in range(len(df_cleaned)):
    s = str(df_cleaned['end_time'][i]) + " 00:00:00"
    l.append(s)

df_cleaned['end_time'] = l
df_cleaned['end_time'] = pd.to_datetime(df_cleaned['end_time'])


# In[9]:


l = list()

for i in range(len(df_cleaned)):
    t = convert(pd.Timedelta(df_cleaned['Start time'][i] - df_cleaned['start_time'][i]).seconds,0)
    l.append(float(t))
    
df_cleaned['start_td'] = l
df_cleaned['start_td'] = df_cleaned['start_td'].round(2)

###############################################################################################

l = list()

for i in range(len(df_cleaned)):
    t = convert(pd.Timedelta(df_cleaned['End'][i] - df_cleaned['end_time'][i]).seconds,0)
    l.append(float(t))
    
df_cleaned['end_td'] = l
df_cleaned['end_td'] = df_cleaned['end_td'].round(2)


# In[10]:


l1 = list()
l2 = list()

for i in range(len(df_cleaned)):
    t1 = convert(pd.Timedelta(df_cleaned['End'][i] - df_cleaned['Start time'][i]).seconds,0)
    t2 = pd.Timedelta(df_cleaned['End'][i] - df_cleaned['Start time'][i]).seconds
    l1.append(t1)
    l2.append(t2)
    
df_cleaned['time_diff'] = l1
df_cleaned['time_diff_cal'] = l2
df_cleaned['time_diff_cal'] = df_cleaned['time_diff_cal'].round(2)


# In[11]:


df_cleaned = df_cleaned[['Activation','Start time','End','start_td','end_td','time_diff','time_diff_cal']]


# In[12]:


print (colored('                                                                        Last Refresh Datetime : ',attrs=['bold'])+colored(Last_refresh_dt, 'blue',attrs=['bold']))


# In[13]:


def graph1(df_n):
    df_n['Activation'] = df_n['Activation'].astype('datetime64')
    df_n.sort_values(by= 'Activation',inplace=True,ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_n['Activation'], y=df_n['time_diff'],
        line=dict(width=2.0, color='rgb(131, 90, 241)'),#rgb(255, 127, 14)
        name = 'Runtime',
        mode='lines+markers'
        ))
         
    fig.add_trace(go.Scatter(
        x=df_n['Activation'], y=df_n['avg_line'],
        line=dict(width=2.0, color='rgb(34, 178, 159)',dash='dot'),#rgb(255, 127, 14)
        name = 'Avg. Runtime',
        mode='lines'
        )),

    fig.update_layout(
    xaxis_title="Load Date",
    yaxis_title="Runtime (in hr.min)",
    
    titlefont=dict(
        size=20
        ),
        title={
        'text': "Daily Trend of Production Jobs Runtime",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
         xaxis=dict(showticklabels=True, automargin=True)
    )
    fig.show()


# In[14]:


def plot1(Date_Range):
    df_n = pd.DataFrame()
    if (Date_Range == 'Last 1 Week'):
        df_n=df_cleaned[df_cleaned['Start time']>np.max(df_cleaned['Start time'])-timedelta(7)]
        df_n['avg_line'] = convert(df_n['time_diff_cal'].mean(),0)
        graph1(df_n)
    elif(Date_Range == 'Last 2 Week'):    
        df_n=df_cleaned[df_cleaned['Start time']>np.max(df_cleaned['Start time'])-timedelta(14)]
        df_n['avg_line'] = convert(df_n['time_diff_cal'].mean(),0)
        graph1(df_n)
    elif(Date_Range == 'Last 3 Week'):
        df_n=df_cleaned[df_cleaned['Start time']>np.max(df_cleaned['Start time'])-timedelta(21)]
        df_n['avg_line'] = convert(df_n['time_diff_cal'].mean(),0)
        graph1(df_n)
    elif(Date_Range == 'Last 4 Week'):
        df_n=df_cleaned[df_cleaned['Start time']>np.max(df_cleaned['Start time'])-timedelta(28)]
        df_n['avg_line'] = convert(df_n['time_diff_cal'].mean(),0)
        graph1(df_n)

        
widgets.interact(plot1,Date_Range=['Last 4 Week','Last 3 Week','Last 2 Week','Last 1 Week']);


# In[15]:


# Production Jobs Trigger (Weekly)


# In[16]:


df3 = pd.read_excel(location + '\\Cleaned_data.xlsx')
df3 = df3[df3['trigger']!='other'].reset_index()
df3['Activation_x'] = pd.to_datetime(df3['Activation_x']).dt.strftime('%d-%b-%y')
df3['Start time_x'] = pd.to_datetime(df3['Start time_x'])
df3['End_x'] = pd.to_datetime(df3['End_x'])


# In[17]:


df_cleaned3 = df3.groupby(['trigger','Activation_x']).agg({'Start time_x': 'min', 'End_x': 'max'}).reset_index()
#df_cleaned3= df3.groupby(['Activation_y','trigger','Start time_y','End_y'])['TableName'].count().reset_index(name='count')


# In[18]:


l1 = list()
l2 = list()

for i in range(len(df_cleaned3)):
    t1 = convert(pd.Timedelta(df_cleaned3['End_x'][i] - df_cleaned3['Start time_x'][i]).seconds,0)
    t2 = pd.Timedelta(df_cleaned3['End_x'][i] - df_cleaned3['Start time_x'][i]).seconds
    l1.append(t1)
    l2.append(t2)
    
df_cleaned3['time_diff'] = l1
df_cleaned3['time_diff_cal'] = l2
df_cleaned3['time_diff_cal'] = df_cleaned3['time_diff_cal'].round(2)


# # <div style="text-align: center"> II. Trigger Level Runtimes </div>

# In[19]:


def graph2(df_cleaned3):
    fig = make_subplots(rows=4,
                    cols=1,
                    y_title='Run Time (in hr.min)',
                    subplot_titles=('Trigger 1 Daily Runtimes',  'Trigger 2 Daily Runtimes', 
                                    'Trigger 3 Daily Runtimes', 'Trigger 4 Daily Runtimes'))

   
    df_cleaned3['Activation_x'] = df_cleaned3['Activation_x'].astype('datetime64')
    br1 = df_cleaned3[df_cleaned3['trigger']=='trigger1'].reset_index()
    br1['avg_line'] = convert(br1['time_diff_cal'].mean(),0)
    br1.sort_values(by= 'Activation_x',inplace=True,ascending=True)

    fig.add_trace(go.Scatter(
        x=br1['Activation_x'], y=br1['time_diff'],
        line=dict(width=2.0, color='rgb(15, 89, 146)'),
        name = 'Exec Time',
        mode='lines+markers'
        ), row=1, col=1),
    fig.add_trace(go.Scatter(
        x=br1['Activation_x'], y=br1['avg_line'],
        line=dict(width=2.0, color='rgb(34, 178, 159)',dash='dot'),
         name = 'Avg. Exec Time',
        mode='lines+markers'
        ), row=1, col=1),

    

    br2 = df_cleaned3[df_cleaned3['trigger']=='trigger2'].reset_index()
    br2['avg_line'] = convert(br2['time_diff_cal'].mean(),0)
    br2.sort_values(by= 'Activation_x',inplace=True,ascending=True)

    fig.add_trace(go.Scatter(
        x=br2['Activation_x'], y=br2['time_diff'],
        line=dict(width=2.0, color='rgb(38, 127, 195)'),
#         name = 'T2 Exec Time',
        mode='lines+markers'
        ), row=2, col=1),
    fig.add_trace(go.Scatter(
        x=br2['Activation_x'], y=br2['avg_line'],
        line=dict(width=2.0, color='rgb(34, 178, 159)',dash='dot'),
#         name = 'Avg. T2 Exec Time',
        mode='lines+markers'
        ), row=2, col=1),    



    br3 = df_cleaned3[df_cleaned3['trigger']=='trigger3'].reset_index()
    br3['avg_line'] = convert(br3['time_diff_cal'].mean(),0)
    br3.sort_values(by= 'Activation_x',inplace=True,ascending=True)

    fig.add_trace(go.Scatter(
        x=br3['Activation_x'], y=br3['time_diff'],
        line=dict(width=2.0, color='rgb(93, 167, 223)'),
#         name = 'T3 Exec Time',
        mode='lines+markers'
        ), row=3, col=1),
    fig.add_trace(go.Scatter(
        x=br3['Activation_x'], y=br3['avg_line'],
        line=dict(width=2.0, color='rgb(34, 178, 159)',dash='dot'),
#         name = 'Avg. T3 Exec Time',
        mode='lines+markers'
        ), row=3, col=1),    

    br4 = df_cleaned3[df_cleaned3['trigger']=='trigger4'].reset_index()
    br4['avg_line'] = convert(br4['time_diff_cal'].mean(),0)
    br4.sort_values(by= 'Activation_x',inplace=True,ascending=True)

    fig.add_trace(go.Scatter(
        x=br4['Activation_x'],y=br4['time_diff'],
        line=dict(width=2.0, color='rgb(116, 187, 242)'),
        name = 'Runtime',
        mode='lines+markers'
        ), row=4, col=1),
    fig.add_trace(go.Scatter(
        x=br4['Activation_x'], y=br4['avg_line'],
        line=dict(width=2.0, color='rgb(34, 178, 159)',dash='dot'),
        name = 'Avg. Runtime',
        mode='lines+markers'
        ), row=4, col=1),    
    fig.update_layout(
    height=900, width=1000,showlegend=False
    )
    fig.show()


# In[20]:


def plot2(Date_Range):
    df_n = pd.DataFrame()
    if (Date_Range == 'Last 1 Week'):
        df_n=df_cleaned3[df_cleaned3['Start time_x']>np.max(df_cleaned3['Start time_x'])-timedelta(7)]  
        graph2(df_n)
    elif(Date_Range == 'Last 2 Week'):    
        df_n=df_cleaned3[df_cleaned3['Start time_x']>np.max(df_cleaned3['Start time_x'])-timedelta(14)]
        graph2(df_n)
    elif(Date_Range == 'Last 3 Week'):
        df_n=df_cleaned3[df_cleaned3['Start time_x']>np.max(df_cleaned3['Start time_x'])-timedelta(21)]
        graph2(df_n)
    elif(Date_Range == 'Last 4 Week'):
        df_n=df_cleaned3[df_cleaned3['Start time_x']>np.max(df_cleaned3['Start time_x'])-timedelta(28)]
        graph2(df_n)

        
widgets.interact(plot2,Date_Range=['Last 4 Week','Last 3 Week','Last 2 Week','Last 1 Week']);


# In[21]:


l = list()

for i in range(len(df3)):
    t = pd.Timedelta(df3['End_x'][i] - df3['Start time_x'][i]).seconds/60
    l.append(t)
    
df3['time_diff'] = l
df3['time_diff'] = df3['time_diff'].round(0)        


# In[22]:


df_grouped = df3.groupby(['Activation_x','TableName','trigger']).agg({'time_diff':'sum'}).reset_index()#[['trigger','TableName','Activation_x','time_diff']]
df_grouped['Activation_x'] = pd.to_datetime(df_grouped['Activation_x'])


# # <div style="text-align: center">III. Trigger level Deep Dives</div>

# In[23]:


global date_filter
date_filter=widgets.DatePicker(description='Select Date');
display(date_filter)


# In[24]:


#df_grouped = df_grouped[df_grouped['Activation_x']==start_date_widget.value]
df_grouped =  df_grouped.rename(columns={"time_diff": "Execution Time", "Name_x": "Job Name"})


# In[25]:


def graph3(df_n):
    df_n = df_n.sort_values(by='Execution Time',ascending = False).head(6)
    fig = px.bar(df_n, x='TableName', y='Execution Time',height = 500,width = 950)
    fig.show()


# In[26]:


def plot3(Trigger):
    df_n = pd.DataFrame()
    if (Trigger == 'Trigger 1'):
        df_n=df_grouped[(df_grouped['trigger'] == 'trigger1')]
        df_n = df_n[df_n['Activation_x'] == date_filter.value] 
        #print(df_n)
        graph3(df_n)
    elif(Trigger == 'Trigger 2'):    
        df_n=df_grouped[df_grouped['trigger'] == 'trigger2']
        df_n = df_n[df_n['Activation_x'] == date_filter.value]  
        graph3(df_n)
    elif(Trigger == 'Trigger 3'):
        df_n=df_grouped[df_grouped['trigger'] == 'trigger3']   
        df_n = df_n[df_n['Activation_x'] == date_filter.value]  
        graph3(df_n)
    elif(Trigger == 'Trigger 4'):
        df_n=df_grouped[df_grouped['trigger'] == 'trigger4']
        df_n = df_n[df_n['Activation_x'] == date_filter.value]  
        graph3(df_n)

        
widgets.interact(plot3,Trigger=['Trigger 1','Trigger 2','Trigger 3','Trigger 4']);


# # <div style="text-align: center">IV. Availability Trend of HROS Data</div>

# In[27]:


df_run = df1

df_run['Activation'] = pd.to_datetime(df_run['Activation']).dt.strftime('%d-%b-%y')
df_run['Start time'] = pd.to_datetime(df_run['Start time'])
df_run['End'] = pd.to_datetime(df_run['End'])

df_run.reset_index(inplace=True)

df_run['start_time'] = df_run['Start time'].dt.date
#df1['end_time'] = df1['End'].dt.date
l = list()

for i in range(len(df_run)):
    s = str(df_run['start_time'][i]) + " 00:00:00"
    l.append(s)

df_run['start_time'] = l
df_run['start_time'] = pd.to_datetime(df_run['start_time'])


df_run['end_time'] = df_run['End'].dt.date
#df1['end_time'] = df1['End'].dt.date
l = list()

for i in range(len(df_run)):
    s = str(df_run['end_time'][i]) + " 00:00:00"
    l.append(s)

df_run['end_time'] = l
df_run['end_time'] = pd.to_datetime(df_run['end_time'])


l = list()

for i in range(len(df_run)):
    t = convert(pd.Timedelta(df_run['Start time'][i] - df_run['start_time'][i]).seconds,0)
    l.append(float(t))
    
df_run['start_td'] = l
df_run['start_td'] = df_run['start_td'].round(2)

###############################################################################################

l = list()

for i in range(len(df_run)):
    t = convert(pd.Timedelta(df_run['End'][i] - df_run['end_time'][i]).seconds,0)
    l.append(float(t))
    
df_run['end_td'] = l
df_run['end_td'] = df_run['end_td'].round(2)


l1 = list()
l2 = list()

for i in range(len(df_run)):
    t1 = convert(pd.Timedelta(df_run['End'][i] - df_run['Start time'][i]).seconds,0)
    t2 = pd.Timedelta(df_run['End'][i] - df_run['Start time'][i]).seconds
    l1.append(t1)
    l2.append(t2)
    
df_run['time_diff'] = l1
df_run['time_diff_cal'] = l2
df_run['time_diff_cal'] = df_run['time_diff_cal'].round(2)


df_run= df_run[['Activation','Start time','End','start_td','end_td','time_diff','time_diff_cal']]


# In[28]:


def graph6(df_run):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_run['Activation'], y=df_run['end_td'],
        line=dict(width=2.0, color='rgb(131, 90, 241)'),#rgb(255, 127, 14)
        name = 'Daily Run Time',
        mode='lines+markers'
        ))
    fig.update_layout(
    xaxis_title="Load Date",
    yaxis_title="Job Completion Time (in hr.min)",
    
     titlefont=dict(
        size=20,
        #color="#7f7f7f",
        ),
        title={
        'text': "Daily Trend of Producton Jobs runtime",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
         xaxis=dict(showticklabels=True, automargin=True,autorange="reversed")
    )
    fig.show()


# In[29]:


def plot6(Date_Range):
    df_n = pd.DataFrame()
    if (Date_Range == 'Last 1 Week'):
        df_n=df_run[df_run['Start time']>np.max(df_run['Start time'])-timedelta(7)]  
        graph6(df_n)
    elif(Date_Range == 'Last 2 Week'):    
        df_n=df_run[df_run['Start time']>np.max(df_run['Start time'])-timedelta(14)]
        graph6(df_n)
    elif(Date_Range == 'Last 3 Week'):
        df_n=df_run[df_run['Start time']>np.max(df_run['Start time'])-timedelta(21)]
        graph6(df_n)
    elif(Date_Range == 'Last 4 Week'):
        df_n=df_run[df_run['Start time']>np.max(df_run['Start time'])-timedelta(28)]
        graph6(df_n)

        
widgets.interact(plot6,Date_Range=['Last 4 Week','Last 3 Week','Last 2 Week','Last 1 Week']);


# In[30]:


df2['Activation'] = pd.to_datetime(df2['Activation']).dt.strftime('%Y-%m-%d')
df_cleaned2 = df2


# In[31]:


df_cleaned2['Start time'] = pd.to_datetime(df_cleaned2['Start time'])
df_cleaned2['End'] = pd.to_datetime(df_cleaned2['End'])
df_cleaned2.reset_index(inplace=True)
#df_cleaned2 = df_cleaned2.dropna(subset=['Start time']).reset_index()


# In[32]:


l = list()

for i in range(len(df_cleaned2)):
    t = pd.Timedelta(df_cleaned2['End'][i] - df_cleaned2['Start time'][i]).seconds/60
    l.append(t)
    
df_cleaned2['time_diff'] = l
df_cleaned2['time_diff'] = df_cleaned2['time_diff'].round(0)


# In[33]:


df_cleaned2 = df_cleaned2[['TableName','Activation','Start time','End','time_diff','Error_Flag','Runtime']]
#df_cleaned2.head()


# In[34]:


df_cleaned2 = df_cleaned2[df_cleaned2['Error_Flag']==1]


# In[35]:


d1 = df_cleaned2.groupby(['TableName'])['TableName'].count().reset_index(name = 'Failure')
d2 = df_cleaned2.groupby(['TableName'])['time_diff'].sum().reset_index(name = 'Total Time Taken')


# In[36]:


df_merged = pd.merge(d1,d2,on='TableName')


# # <div style="text-align: center">V. View into Failed Jobs</div>

# In[37]:


def graph4(df_n):
    fig = px.scatter(df_n, x="Total Time Taken", y="Failure",
                  hover_name="TableName",size="Failure",
                 color="TableName",width= 1000,height = 400,
                  size_max=30)
    fig.update_layout(
                      xaxis_title="Runtime(in mins.)",
                      yaxis_title="#Failures",
                   titlefont=dict(
                        size=20
                                  ),
                      title={
                          'text': "Failed Jobs Summary",
                           'y':0.9,
                           'x':0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'},
                      xaxis=dict(showticklabels=True, automargin=True)
                      )
    fig.show()


# In[38]:


def plot4(Failure):
    df_n = pd.DataFrame()
    if (Failure == 'Failed less than 3'):
        df_n=df_merged[df_merged['Failure'] <3]   
        graph4(df_n)
    elif(Failure == 'Failed less than 5'):    
        df_n=df_merged[(df_merged['Failure'] >= 3) & (df_merged['Failure'] < 5)]  
        graph4(df_n)
    elif(Failure == 'Failed greater than 5'):
        df_n=df_merged[df_merged['Failure'] >= 5] 
        graph4(df_n) 
    else:
        df_n = df_merged
        graph4(df_n)
        
widgets.interact(plot4,Failure=['Failed less than 3','Failed less than 5','Failed greater than 5','All']);


# In[39]:


df_top_failed = df_merged.sort_values(by="Failure",ascending=False)
df_top_failed = df_top_failed[df_top_failed['Failure']>5]['TableName']


# In[40]:


df_top_failed = pd.merge(df_top_failed,df_cleaned2,on='TableName')


# In[41]:


df_top_failed.sort_values(by='time_diff',ascending=False,inplace=True)


# # <div style="text-align: center">VI. Table Failed showing Date and Execution Time</div>

# In[42]:


def graph5(df):
    fig = go.Figure(data=[go.Table(
    header=dict(values=['Table Name', 'Start Time','End Time','Run Time(in min.)']),
    cells=dict(values=[df['TableName'],df['Start time'].dt.strftime('%d-%b-%y %r'),df['End'].dt.strftime('%d-%b-%y %r'),df['time_diff'].round(0)], # 2nd column
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
    ])

    fig.show()                      


# In[43]:


def plot5(Trigger):
    df_n = pd.DataFrame()
    if (Trigger == 'Top 5'):
        df_n=df_top_failed.head(5)  
        graph5(df_n)
    elif(Trigger == 'Top 10'):    
        df_n=df_top_failed.head(10)
        graph5(df_n)
    elif(Trigger == 'Top 15'):
        df_n=df_top_failed.head(15)   
        graph5(df_n)


        
widgets.interact(plot5,Trigger=['Top 5','Top 10','Top 15']);

