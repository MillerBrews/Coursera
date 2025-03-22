#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

year_list = [i for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard, with style
    html.H1("Automobile Statistics Dashboard",
            style={'textAlign': 'center',
            'color': '#503D36', 'font-size': 24}),
    #TASK 2.2: Add two dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            placeholder='Select a report type',
            value='Select Statistics',
            style={'width':'80%', 'padding':'3px',
                   'font-size':'20px', 'text-align-last':'center'}
        )
    ]),
    html.Div(dcc.Dropdown(
            id='select-year',
            options=year_list,#[{'label':i, 'value':i} for i in year_list],
            placeholder='Select-year',
            value='Select-year',
            style={'width':'80%', 'padding':'3px',
                   'font-size':'20px', 'text-align-last':'center'}
        )),
    html.Div([#TASK 2.3: Add a division for output display
    html.Div(id='output-container', className='chart-grid', style={'display':'flex'}),])
])

#TASK 2.4: Creating Callbacks
@app.callback(Output(component_id='select-year', component_property='disabled'),
            Input(component_id='dropdown-statistics', component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics': 
        return False
    else: 
        return True

#Callback for plotting
@app.callback(Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')])

def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        #TASK 2.5: Create and display graphs for Recession Report Statistics
        #Plot 1, Automobile sales fluctuate over Recession Period (year-wise)
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                title="Average Automobile Sales Fluctuation over Recession Period"))

        #Plot 2, Calculate the average number of vehicles sold by vehicle type
        #Hint:Use Vehicle_Type and Automobile_Sales columns
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2  = dcc.Graph(figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales',
                title="Average Automobile Sales by Vehicle Type"))
        
        #Plot 3, Pie chart for total expenditure share by vehicle type during recessions
	    #Hint:Use Vehicle_Type and Advertising_Expenditure columns
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(exp_rec, values='Advertising_Expenditure',
                names='Vehicle_Type', title="Expenditure Share by Vehicle Type During Recessions"))

        #Plot 4, Bar chart for the effect of unemployment rate on vehicle type and sales
    	#Hint:Use unemployment_rate,Vehicle_Type and Automobile_Sales columns
        unemp_data = recession_data.groupby(['unemployment_rate','Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(unemp_data, x='unemployment_rate', y='Vehicle_Type',
                color='Vehicle_Type',
                labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return [
            html.Div(className='chart-item', children=[R_chart1,R_chart2]),
            html.Div(className='chart-item', children=[R_chart3,R_chart4])
            ]

    # TASK 2.6: Create and display plots for Yearly Report Statistics
    elif (input_year and selected_statistics=='Yearly Statistics'):
        yearly_data = data[data['Year'] == input_year]

        #Plot 1, Yearly Automobile sales using line chart for the whole period
        #Hint:Use the columns Year and Automobile_Sales.
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales',
                title="Yearly Average Automobile Sales"))
            
        #Plot 2, Total Monthly Automobile sales using line chart
    	#Hint:Use the columns Month and Automobile_Sales.
        # mas=data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(yearly_data, x='Month', y='Automobile_Sales',
                title=f"Monthly Automobile Sales for {input_year}"))

        #Plot 3, Bar chart for average number of vehicles sold during the given year
        #Hint:Use the columns Year and Automobile_Sales
        avr_vdata=data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Year', y='Automobile_Sales',
                title=f'Average Vehicles Sold by Vehicle Type in {input_year}'))

        #Plot 4, Total Advertisement Expenditure for each vehicle using pie chart
        #Hint:Use the columns Vehicle_Type and Advertising_Expenditure
        exp_data=yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, values='Advertising_Expenditure',
                names='Vehicle_Type', title=f"Total Advertising Expenditure for Vehicle Type in {input_year}"))

        #TASK 2.6: Returning the graphs for displaying Yearly data
        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2]),
            html.Div(className='chart-item', children=[R_chart3, R_chart4])
        ]

    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
