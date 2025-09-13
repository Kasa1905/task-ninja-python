import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path

class SalesDashboard:
    def __init__(self, data_file: str):
        """Initialize dashboard with data file."""
        self.df = pd.read_csv(data_file)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df['Year'] = self.df['Date'].dt.year
        self.df['Month'] = self.df['Date'].dt.month
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()

    def create_sales_chart(self, selected_view: str) -> go.Figure:
        """Create sales visualization based on selected view."""
        if selected_view == 'Monthly Trend':
            monthly = self.df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
            monthly['Date'] = pd.to_datetime(monthly[['Year', 'Month']].assign(DAY=1))
            fig = px.line(monthly, x='Date', y='Sales',
                         title='Monthly Sales Trend',
                         labels={'Sales': 'Total Sales', 'Date': 'Month'})

        elif selected_view == 'Product Performance':
            product_sales = self.df.groupby('Product')['Sales'].sum().reset_index()
            fig = px.pie(product_sales, values='Sales', names='Product',
                        title='Sales by Product')

        elif selected_view == 'Regional Analysis':
            region_sales = self.df.groupby('Region')['Sales'].sum().reset_index()
            fig = px.bar(region_sales, x='Region', y='Sales',
                        title='Sales by Region')

        else:  # Year-over-Year
            yearly = self.df.groupby('Year')['Sales'].sum().reset_index()
            fig = px.bar(yearly, x='Year', y='Sales',
                        title='Yearly Sales Comparison')

        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=50, l=10, r=10, b=10),
            showlegend=True
        )
        return fig

    def create_kpi_cards(self) -> html.Div:
        """Create KPI metrics cards."""
        total_sales = self.df['Sales'].sum()
        avg_sales = self.df['Sales'].mean()
        num_products = self.df['Product'].nunique()
        num_regions = self.df['Region'].nunique()

        kpi_style = {
            'textAlign': 'center',
            'padding': '20px',
            'margin': '10px',
            'backgroundColor': '#f8f9fa',
            'borderRadius': '5px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        }

        return html.Div([
            html.Div([
                html.H4('Total Sales'),
                html.H2(f'${total_sales:,.0f}')
            ], style=kpi_style),
            html.Div([
                html.H4('Average Sale'),
                html.H2(f'${avg_sales:,.0f}')
            ], style=kpi_style),
            html.Div([
                html.H4('Products'),
                html.H2(f'{num_products}')
            ], style=kpi_style),
            html.Div([
                html.H4('Regions'),
                html.H2(f'{num_regions}')
            ], style=kpi_style),
        ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '20px'})

    def setup_layout(self):
        """Set up the dashboard layout."""
        self.app.layout = html.Div([
            # Header
            html.H1('Sales Analytics Dashboard',
                   style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),

            # KPI Cards
            self.create_kpi_cards(),

            # Controls
            html.Div([
                dcc.Dropdown(
                    id='view-selector',
                    options=[
                        {'label': 'Monthly Trend', 'value': 'Monthly Trend'},
                        {'label': 'Product Performance', 'value': 'Product Performance'},
                        {'label': 'Regional Analysis', 'value': 'Regional Analysis'},
                        {'label': 'Year-over-Year', 'value': 'Year-over-Year'}
                    ],
                    value='Monthly Trend',
                    style={'width': '50%', 'margin': 'auto'}
                )
            ], style={'marginBottom': '20px'}),

            # Chart
            dcc.Graph(id='main-chart'),

        ], style={'padding': '20px'})

    def setup_callbacks(self):
        """Set up interactive callbacks."""
        @self.app.callback(
            Output('main-chart', 'figure'),
            [Input('view-selector', 'value')]
        )
        def update_chart(selected_view):
            return self.create_sales_chart(selected_view)

    def run_server(self, debug: bool = True, port: int = 8050):
        """Run the dashboard server."""
        self.app.run_server(debug=debug, port=port)

def main():
    # Get the current directory
    current_dir = Path(__file__).parent
    data_file = current_dir / 'sample_sales_data.csv'
    
    # Initialize and run dashboard
    dashboard = SalesDashboard(str(data_file))
    dashboard.run_server()

if __name__ == '__main__':
    main()
