import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

# Load the CSV data into a DataFrame
sales_data = pd.read_csv('C:\\Users\\hamze\\Desktop\\NG BI Guru\\Video 17 AI Vs BI specialist\\Sales_Hierarchy.csv')

# Unique list of countries, products, and years for the dropdown filters
countries = sales_data['Country'].unique()
products = sales_data['Product'].unique()
years = sales_data['Year'].unique()

# Initiating the Dash app
app = dash.Dash(__name__)

# Defining the layout of the dashboard
app.layout = html.Div([
    # Filters
    html.Div([
        html.Label('Country:'),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in countries],
            value=countries,
            multi=True
        ),
        html.Label('Product:'),
        dcc.Dropdown(
            id='product-dropdown',
            options=[{'label': product, 'value': product} for product in products],
            value=products,
            multi=True
        ),
        html.Label('Year:'),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in years],
            value=years,
            multi=True
        ),
    ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'space-between'}),

    # Donut Visuals
    html.Div([
        dcc.Graph(id='sales-per-year', clickData=None),
        dcc.Graph(id='sales-per-country', clickData=None),
        dcc.Graph(id='sales-per-product', clickData=None)
    ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'space-between'}),
])

# Callbacks for the donut visuals
@app.callback(
    [Output('sales-per-year', 'figure'),
     Output('sales-per-country', 'figure'),
     Output('sales-per-product', 'figure')],
    [Input('country-dropdown', 'value'),
     Input('product-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('sales-per-year', 'clickData'),
     Input('sales-per-country', 'clickData'),
     Input('sales-per-product', 'clickData')]
)
def update_visuals(selected_countries, selected_products, selected_years, year_click_data, country_click_data, product_click_data):
    filtered_data = sales_data[
        (sales_data['Country'].isin(selected_countries)) &
        (sales_data['Product'].isin(selected_products)) &
        (sales_data['Year'].isin(selected_years))
    ]

    # Donut Visual 1: Sales per year or quarter (drill-through)
    if year_click_data:
        clicked_year = year_click_data['points'][0]['label']
        fig1 = px.pie(
            filtered_data[filtered_data['Year'] == int(clicked_year)].groupby('Quarter').sum().reset_index(),
            names='Quarter',
            values='Sales',
            hole=0.3,
            title=f'Sales in {clicked_year} by Quarter'
        )
    else:
        fig1 = px.pie(
            filtered_data.groupby('Year').sum().reset_index(),
            names='Year',
            values='Sales',
            hole=0.3,
            title='Overall Sales Per Year'
        )

    # Donut Visual 2: Sales per country or product (drill-through)
    if country_click_data:
        clicked_country = country_click_data['points'][0]['label']
        fig2 = px.pie(
            filtered_data[filtered_data['Country'] == clicked_country].groupby('Product').sum().reset_index(),
            names='Product',
            values='Sales',
            hole=0.3,
            title=f'Sales in {clicked_country} by Product'
        )
    else:
        fig2 = px.pie(
            filtered_data.groupby('Country').sum().reset_index(),
            names='Country',
            values='Sales',
            hole=0.3,
            title='Overall Sales Per Country'
        )

    # Donut Visual 3: Sales per product or country (drill-through)
    if product_click_data:
        clicked_product = product_click_data['points'][0]['label']
        fig3 = px.pie(
            filtered_data[filtered_data['Product'] == clicked_product].groupby('Country').sum().reset_index(),
            names='Country',
            values='Sales',
            hole=0.3,
            title=f'Sales of {clicked_product} by Country'
        )
    else:
        fig3 = px.pie(
            filtered_data.groupby('Product').sum().reset_index(),
            names='Product',
            values='Sales',
            hole=0.3,
            title='Overall Sales Per Product'
        )

    return fig1, fig2, fig3

# Running the app
if __name__ == '__main__':
    app.run_server(debug=True)
