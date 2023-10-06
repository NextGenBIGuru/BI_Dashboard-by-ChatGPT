import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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
            value=countries,  # default value
            multi=True  # Allow multiple selection
        ),
        html.Label('Product:'),
        dcc.Dropdown(
            id='product-dropdown',
            options=[{'label': product, 'value': product} for product in products],
            value=products,  # default value
            multi=True  # Allow multiple selection
        ),
        html.Label('Year:'),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in years],
            value=years,  # default value
            multi=True  # Allow multiple selection
        ),
    ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'space-between'}),

    # Donut Visuals
    html.Div([
        dcc.Graph(id='sales-per-year'),
        dcc.Graph(id='sales-per-country'),
        dcc.Graph(id='sales-per-product')
    ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'space-between'}),
])

# Callbacks for the donut visuals
@app.callback(
    [Output('sales-per-year', 'figure'),
     Output('sales-per-country', 'figure'),
     Output('sales-per-product', 'figure')],
    [Input('country-dropdown', 'value'),
     Input('product-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_visuals(selected_countries, selected_products, selected_years):
    # Filter data based on selections
    filtered_data = sales_data[
        (sales_data['Country'].isin(selected_countries)) &
        (sales_data['Product'].isin(selected_products)) &
        (sales_data['Year'].isin(selected_years))
    ]

    # Donut Visual 1: Overall sales per year
    fig1 = px.pie(
        filtered_data.groupby('Year').sum().reset_index(),
        names='Year',
        values='Sales',
        hole=0.3,
        title='Overall Sales Per Year'
    )

    # Donut Visual 2: Overall sales per country
    fig2 = px.pie(
        filtered_data.groupby('Country').sum().reset_index(),
        names='Country',
        values='Sales',
        hole=0.3,
        title='Overall Sales Per Country'
    )

    # Donut Visual 3: Overall sales per product
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
