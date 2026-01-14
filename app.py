import dash
from dash import dcc, html, callback, Input
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

# Define custom styles
colors = {
    'background': '#fafafa',
    'primary': '#e91e63',
    'primary_light': '#f06292',
    'secondary': '#2196F3',
    'text_dark': '#212121',
    'text_light': '#757575',
    'card_bg': '#ffffff',
    'border': '#e0e0e0'
}

# Define the app layout
app.layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.H1('Pink Morsel Sales Analysis', style={
                'textAlign': 'center',
                'color': colors['primary'],
                'marginBottom': '10px',
                'fontSize': '2.5em',
                'fontWeight': 'bold'
            }),
            html.P('Visualizing sales trends to answer: Were sales higher before or after the Pink Morsel price increase on January 15, 2021?', 
                style={
                    'textAlign': 'center',
                    'fontSize': '16px',
                    'color': colors['text_light'],
                    'marginBottom': '0px'
                })
        ], style={
            'maxWidth': '1200px',
            'margin': '0 auto'
        })
    ], style={
        'backgroundColor': colors['background'],
        'padding': '40px 20px',
        'borderBottom': f'3px solid {colors["primary"]}',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    }),
    
    # Main content container
    html.Div([
        # Filters section
        html.Div([
            html.Div([
                html.H3('Filter by Region:', style={
                    'color': colors['text_dark'],
                    'marginBottom': '15px',
                    'fontSize': '1.1em',
                    'fontWeight': '600'
                }),
                dcc.RadioItems(
                    id='region-selector',
                    options=[
                        {'label': ' All Regions', 'value': 'all'},
                        {'label': ' North', 'value': 'north'},
                        {'label': ' South', 'value': 'south'},
                        {'label': ' East', 'value': 'east'},
                        {'label': ' West', 'value': 'west'}
                    ],
                    value='all',
                    inline=True,
                    style={
                        'display': 'flex',
                        'gap': '20px'
                    },
                    labelStyle={
                        'display': 'inline-block',
                        'marginRight': '0px',
                        'cursor': 'pointer',
                        'color': colors['text_dark']
                    }
                )
            ], style={
                'backgroundColor': colors['card_bg'],
                'padding': '20px',
                'borderRadius': '8px',
                'border': f'1px solid {colors["border"]}',
                'marginBottom': '20px',
                'boxShadow': '0 1px 3px rgba(0,0,0,0.05)'
            })
        ], style={
            'maxWidth': '1200px',
            'margin': '0 auto',
            'padding': '20px'
        }),
        
        # Chart container
        html.Div([
            dcc.Graph(id='sales-chart', style={
                'border': f'1px solid {colors["border"]}',
                'borderRadius': '8px',
                'overflow': 'hidden'
            })
        ], style={
            'backgroundColor': colors['card_bg'],
            'padding': '20px',
            'borderRadius': '8px',
            'boxShadow': '0 1px 3px rgba(0,0,0,0.05)',
            'maxWidth': '1200px',
            'margin': '0 auto 20px auto'
        }),
        
        # Summary stats
        html.Div(id='summary-stats', style={
            'maxWidth': '1200px',
            'margin': '0 auto'
        })
    ], style={
        'padding': '0px 20px 20px 20px'
    })
], style={
    'fontFamily': '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
    'margin': '0px',
    'padding': '0px',
    'backgroundColor': colors['background'],
    'minHeight': '100vh'
})

# Callback to update the chart
@app.callback(
    [dash.Output('sales-chart', 'figure'),
     dash.Output('summary-stats', 'children')],
    [Input('region-selector', 'value')]
)
def update_chart(selected_region):
    # Filter data by region
    if selected_region == 'all':
        filtered_df = df
        title_suffix = ' - All Regions'
    else:
        filtered_df = df[df['Region'] == selected_region]
        title_suffix = f' - {selected_region.capitalize()}'
    
    # Create line chart
    fig = go.Figure()
    
    # Price increase date
    price_increase_date = pd.to_datetime('2021-01-15')
    
    # Define region colors
    region_colors = {
        'north': '#FF6B6B',
        'south': '#4ECDC4',
        'east': '#45B7D1',
        'west': '#FFA07A'
    }
    
    if selected_region == 'all':
        # Add traces for each region
        for region in sorted(df['Region'].unique()):
            region_data = df[df['Region'] == region].sort_values('Date')
            fig.add_trace(go.Scatter(
                x=region_data['Date'],
                y=region_data['Sales'],
                mode='lines+markers',
                name=region.capitalize(),
                line=dict(
                    width=2.5,
                    color=region_colors.get(region, '#999')
                ),
                marker=dict(size=4),
                hovertemplate='<b>%{fullData.name}</b><br>Date: %{x|%Y-%m-%d}<br>Sales: $%{y:,.2f}<extra></extra>'
            ))
    else:
        # Add single trace for selected region
        region_data = filtered_df.sort_values('Date')
        fig.add_trace(go.Scatter(
            x=region_data['Date'],
            y=region_data['Sales'],
            mode='lines+markers',
            name=selected_region.capitalize(),
            line=dict(
                width=3,
                color=region_colors.get(selected_region, '#999')
            ),
            marker=dict(size=5),
            hovertemplate='<b>%{fullData.name}</b><br>Date: %{x|%Y-%m-%d}<br>Sales: $%{y:,.2f}<extra></extra>'
        ))
    
    # Add vertical line at price increase date
    fig.add_vline(
        x=price_increase_date,
        line_dash="dash",
        line_color=colors['primary'],
        line_width=2,
        annotation_text="Price Increase",
        annotation_position="top right",
        annotation_font_size=12,
        annotation_font_color=colors['primary']
    )
    
    # Update layout with improved styling
    fig.update_layout(
        title={
            'text': f'Daily Pink Morsel Sales{title_suffix}',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': colors['text_dark']}
        },
        xaxis_title='Date',
        yaxis_title='Sales ($)',
        hovermode='x unified',
        template='plotly_white',
        height=500,
        font=dict(size=12, family='Arial, sans-serif'),
        plot_bgcolor='#fafafa',
        paper_bgcolor='#ffffff',
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#e0e0e0',
            showline=True,
            linewidth=1,
            linecolor='#bdbdbd'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#e0e0e0',
            showline=True,
            linewidth=1,
            linecolor='#bdbdbd'
        ),
        legend=dict(
            x=0.01,
            y=0.99,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#bdbdbd',
            borderwidth=1
        )
    )
    
    # Calculate summary statistics
    before_price_increase = filtered_df[filtered_df['Date'] < price_increase_date]['Sales'].sum()
    after_price_increase = filtered_df[filtered_df['Date'] >= price_increase_date]['Sales'].sum()
    
    # Calculate average daily sales
    before_avg = filtered_df[filtered_df['Date'] < price_increase_date]['Sales'].mean()
    after_avg = filtered_df[filtered_df['Date'] >= price_increase_date]['Sales'].mean()
    
    # Determine if sales increased or decreased
    change_percent = ((after_avg - before_avg) / before_avg) * 100 if before_avg > 0 else 0
    
    # Determine color based on change
    change_color = colors['primary'] if change_percent > 0 else '#f44336'
    change_indicator = '📈 Increased' if change_percent > 0 else '📉 Decreased'
    
    summary = html.Div([
        html.H2('Key Findings', style={
            'color': colors['primary'],
            'textAlign': 'center',
            'marginBottom': '30px',
            'fontSize': '1.8em'
        }),
        html.Div([
            html.Div([
                html.Div([
                    html.H4('Before Price Increase', style={
                        'color': colors['text_dark'],
                        'marginBottom': '15px',
                        'borderBottom': f'2px solid {colors["primary"]}',
                        'paddingBottom': '10px'
                    }),
                    html.P(f'Total Sales', style={'color': colors['text_light'], 'fontSize': '12px', 'marginBottom': '5px'}),
                    html.P(f'${before_price_increase:,.2f}', style={
                        'fontSize': '24px',
                        'fontWeight': 'bold',
                        'color': colors['secondary'],
                        'marginBottom': '15px'
                    }),
                    html.P(f'Avg Daily Sales', style={'color': colors['text_light'], 'fontSize': '12px', 'marginBottom': '5px'}),
                    html.P(f'${before_avg:,.2f}', style={
                        'fontSize': '20px',
                        'fontWeight': 'bold',
                        'color': colors['text_dark']
                    })
                ], style={
                    'backgroundColor': '#f5f5f5',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'textAlign': 'center'
                })
            ], style={'flex': '1', 'marginRight': '15px'}),
            
            html.Div([
                html.Div([
                    html.H4('After Price Increase', style={
                        'color': colors['text_dark'],
                        'marginBottom': '15px',
                        'borderBottom': f'2px solid {colors["primary"]}',
                        'paddingBottom': '10px'
                    }),
                    html.P(f'Total Sales', style={'color': colors['text_light'], 'fontSize': '12px', 'marginBottom': '5px'}),
                    html.P(f'${after_price_increase:,.2f}', style={
                        'fontSize': '24px',
                        'fontWeight': 'bold',
                        'color': colors['secondary'],
                        'marginBottom': '15px'
                    }),
                    html.P(f'Avg Daily Sales', style={'color': colors['text_light'], 'fontSize': '12px', 'marginBottom': '5px'}),
                    html.P(f'${after_avg:,.2f}', style={
                        'fontSize': '20px',
                        'fontWeight': 'bold',
                        'color': colors['text_dark']
                    })
                ], style={
                    'backgroundColor': '#f5f5f5',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'textAlign': 'center'
                })
            ], style={'flex': '1'})
        ], style={
            'display': 'flex',
            'marginBottom': '30px',
            'gap': '15px'
        }),
        
        html.Div([
            html.Div([
                html.H3(f'{change_indicator}', style={
                    'color': change_color,
                    'marginBottom': '10px',
                    'fontSize': '1.3em'
                }),
                html.H2(f'{change_percent:+.1f}%', style={
                    'color': change_color,
                    'marginBottom': '5px',
                    'fontSize': '2.5em',
                    'fontWeight': 'bold'
                }),
                html.P('Change in Average Daily Sales', style={
                    'color': colors['text_light'],
                    'fontSize': '12px'
                })
            ], style={
                'backgroundColor': '#ffffff',
                'padding': '30px',
                'borderRadius': '8px',
                'border': f'2px solid {change_color}',
                'textAlign': 'center'
            })
        ], style={
            'maxWidth': '300px',
            'margin': '0 auto'
        })
    ], style={
        'backgroundColor': colors['card_bg'],
        'padding': '30px',
        'borderRadius': '8px',
        'boxShadow': '0 1px 3px rgba(0,0,0,0.05)',
        'border': f'1px solid {colors["border"]}'
    })
    
    return fig, summary

if __name__ == '__main__':
    app.run_server(debug=True)
