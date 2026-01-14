import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd

# Load the processed sales data
df = pd.read_csv('data/processed_sales_data.csv')

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Sort by date
df = df.sort_values('Date')

# Create the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1('Pink Morsel Sales Analysis', style={
            'textAlign': 'center',
            'color': '#e91e63',
            'marginBottom': 10
        }),
        html.P('Visualizing sales trends to answer: Were sales higher before or after the Pink Morsel price increase on January 15, 2021?', 
            style={
                'textAlign': 'center',
                'fontSize': 16,
                'color': '#666'
            })
    ], style={
        'backgroundColor': '#f5f5f5',
        'padding': '20px',
        'marginBottom': '20px',
        'borderBottom': '2px solid #e91e63'
    }),
    
    # Chart container
    html.Div([
        dcc.Graph(id='sales-chart')
    ], style={
        'padding': '20px'
    }),
    
    # Summary stats
    html.Div(id='summary-stats', style={
        'padding': '20px',
        'backgroundColor': '#f5f5f5',
        'borderTop': '2px solid #e91e63',
        'marginTop': '20px'
    })
], style={
    'fontFamily': 'Arial, sans-serif',
    'margin': '0px',
    'padding': '0px'
})

# Callback to update the chart
@app.callback(
    [dash.Output('sales-chart', 'figure'),
     dash.Output('summary-stats', 'children')],
    []
)
def update_chart():
    # Create line chart with trace for each region
    fig = go.Figure()
    
    # Price increase date
    price_increase_date = pd.to_datetime('2021-01-15')
    
    for region in df['Region'].unique():
        region_data = df[df['Region'] == region].sort_values('Date')
        fig.add_trace(go.Scatter(
            x=region_data['Date'],
            y=region_data['Sales'],
            mode='lines+markers',
            name=region.capitalize(),
            line=dict(width=2)
        ))
    
    # Add vertical line at price increase date
    fig.add_vline(
        x=price_increase_date,
        line_dash="dash",
        line_color="red",
        annotation_text="Price Increase (Jan 15, 2021)",
        annotation_position="top right"
    )
    
    # Update layout
    fig.update_layout(
        title='Daily Pink Morsel Sales Over Time',
        xaxis_title='Date',
        yaxis_title='Sales ($)',
        hovermode='x unified',
        template='plotly_white',
        height=500,
        font=dict(size=12)
    )
    
    # Calculate summary statistics
    before_price_increase = df[df['Date'] < price_increase_date]['Sales'].sum()
    after_price_increase = df[df['Date'] >= price_increase_date]['Sales'].sum()
    
    # Calculate average daily sales
    before_avg = df[df['Date'] < price_increase_date]['Sales'].mean()
    after_avg = df[df['Date'] >= price_increase_date]['Sales'].mean()
    
    # Determine if sales increased or decreased
    change_percent = ((after_avg - before_avg) / before_avg) * 100
    
    summary = html.Div([
        html.H2('Key Findings', style={'color': '#e91e63'}),
        html.Div([
            html.Div([
                html.H4('Before Price Increase (Before Jan 15, 2021)'),
                html.P(f'Total Sales: ${before_price_increase:,.2f}'),
                html.P(f'Average Daily Sales: ${before_avg:,.2f}')
            ], style={'flex': '1', 'marginRight': '20px'}),
            html.Div([
                html.H4('After Price Increase (On/After Jan 15, 2021)'),
                html.P(f'Total Sales: ${after_price_increase:,.2f}'),
                html.P(f'Average Daily Sales: ${after_avg:,.2f}')
            ], style={'flex': '1'})
        ], style={'display': 'flex'}),
        html.H3(f'Average Daily Sales Change: {change_percent:+.1f}%', style={
            'color': '#e91e63' if change_percent > 0 else '#f44336',
            'marginTop': '20px'
        })
    ])
    
    return fig, summary

if __name__ == '__main__':
    app.run_server(debug=True)
