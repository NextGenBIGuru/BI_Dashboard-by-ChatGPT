import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the CSV data into a DataFrame
sales_data = pd.read_csv('C:\\Users\\hamze\\Desktop\\NG BI Guru\\Video 17 AI Vs BI specialist\\Sales_Hierarchy.csv')

# Initiating the Dash app
app = dash.Dash(__name__)

# Defining the layout of the dashboard
app.layout = html.Div([
    # Filter for Year
    html.Div([
        html.Label('Select Year:'),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in sales_data['Year'].unique()],
            value=sales_data['Year'].unique()[0],  # default value
        ),
    ]),

    # Donut Visual: Overall sales per year
    dcc.Graph(id='sales-per-year')
])

# Callback for the donut visual
@app.callback(
    Output('sales-per-year', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_visual(selected_year):
    # Filter data based on selected year
    filtered_data = sales_data[sales_data['Year'] == selected_year]

    # Donut Visual: Overall sales per year
    fig = px.pie(
        filtered_data.groupby('Product').sum().reset_index(),
        names='Product',
        values='Sales',
        hole=0.3,
        title=f'Overall Sales Per Product for {selected_year}'
    )

    return fig

# Running the app
if __name__ == '__main__':
    app.run_server(debug=True)
