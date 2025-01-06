import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class VisualizationTheme:
    """Central theme configuration for all visualizations"""
    TEMPLATE = "plotly_dark"
    COLORS = {
        'primary': '#00B4D8',
        'secondary': '#90E0EF',
        'accent': '#CAF0F8',
        'background': '#0D1B2A',
        'grid': '#1B263B',
        'text': '#E0E1DD',
        'warning': '#FF9F1C',
        'error': '#E63946'
    }
    
    # Typography system
    TYPOGRAPHY = {
        'font_family': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
        'sizes': {
            'xs': '12px',
            'sm': '14px',
            'base': '16px',
            'lg': '18px',
            'xl': '24px',
            '2xl': '30px',
        },
        'weights': {
            'normal': '400',
            'medium': '500',
            'semibold': '600',
            'bold': '700',
        }
    }
    
    # Update chart config for better consistency
    CHART_CONFIG = {
        'height': 400,  # Increased height
        'margin': dict(l=40, r=20, t=40, b=40),
        'paper_bgcolor': 'rgba(13,27,42,0.8)',
        'plot_bgcolor': 'rgba(27,38,59,0.8)',
        'modebar_bgcolor': 'rgba(13,27,42,0.8)',
        'modebar_color': '#E0E1DD',
        'modebar_activecolor': '#00B4D8'
    }

    # Enhanced interaction config
    INTERACTION_CONFIG = {
        'displayModeBar': True,
        'scrollZoom': True,
        'displaylogo': False,
        'modeBarButtonsToAdd': ['select2d', 'lasso2d', 'resetScale2d'],
        'modeBarButtonsToRemove': ['autoScale2d'],
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'chart',
            'height': 800,
            'width': 1200,
            'scale': 2
        }
    }

    @classmethod
    def get_css(cls):
        """Returns complete CSS styling for the app"""
        return f"""
        <style>
        /* Global Typography */
        .main {{
            font-family: {cls.TYPOGRAPHY['font_family']};
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['text']};
        }}

        /* Headings */
        h1 {{
            font-size: {cls.TYPOGRAPHY['sizes']['2xl']};
            font-weight: {cls.TYPOGRAPHY['weights']['bold']};
            color: {cls.COLORS['text']};
            margin: 1.5rem 0;
        }}

        h2 {{
            font-size: {cls.TYPOGRAPHY['sizes']['xl']};
            font-weight: {cls.TYPOGRAPHY['weights']['semibold']};
            color: {cls.COLORS['text']};
            margin: 1.25rem 0;
        }}

        h3 {{
            font-size: {cls.TYPOGRAPHY['sizes']['lg']};
            font-weight: {cls.TYPOGRAPHY['weights']['semibold']};
            color: {cls.COLORS['text']};
            margin: 1rem 0;
        }}

        h4 {{
            font-size: {cls.TYPOGRAPHY['sizes']['base']};
            font-weight: {cls.TYPOGRAPHY['weights']['medium']};
            color: {cls.COLORS['secondary']};
            margin: 0.75rem 0;
        }}

        /* Components */
        .stButton>button {{
            font-family: {cls.TYPOGRAPHY['font_family']};
            font-size: {cls.TYPOGRAPHY['sizes']['base']};
            font-weight: {cls.TYPOGRAPHY['weights']['medium']};
            background-color: {cls.COLORS['primary']};
            color: white;
            border-radius: 5px;
            padding: 0.75rem 1.5rem;
            border: none;
            width: 100%;
        }}

        .stMetric {{
            background-color: rgba(27,38,59,0.5);
            padding: 1.5rem;
            border-radius: 8px;
            margin: 0.75rem 0;
            border: 1px solid {cls.COLORS['grid']};
        }}

        .metric-label {{
            font-size: {cls.TYPOGRAPHY['sizes']['sm']};
            font-weight: {cls.TYPOGRAPHY['weights']['medium']};
            color: {cls.COLORS['secondary']};
        }}

        .metric-value {{
            font-size: {cls.TYPOGRAPHY['sizes']['xl']};
            font-weight: {cls.TYPOGRAPHY['weights']['bold']};
            color: {cls.COLORS['text']};
        }}

        .stDataFrame {{
            font-size: {cls.TYPOGRAPHY['sizes']['sm']};
            background-color: {cls.COLORS['background']};
            border-radius: 5px;
            padding: 1rem;
        }}

        .stTextArea textarea {{
            font-family: {cls.TYPOGRAPHY['font_family']};
            font-size: {cls.TYPOGRAPHY['sizes']['base']};
            line-height: 1.6;
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['text']};
            padding: 1rem;
            border: 1px solid {cls.COLORS['grid']};
            border-radius: 5px;
        }}

        /* Section Headers */
        .section-title {{
            font-size: {cls.TYPOGRAPHY['sizes']['lg']};
            font-weight: {cls.TYPOGRAPHY['weights']['semibold']};
            color: {cls.COLORS['text']};
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid {cls.COLORS['primary']};
        }}

        /* Expander Headers */
        .streamlit-expanderHeader {{
            font-size: {cls.TYPOGRAPHY['sizes']['base']};
            font-weight: {cls.TYPOGRAPHY['weights']['medium']};
            color: {cls.COLORS['text']};
        }}
        </style>
        """

    @classmethod
    def apply_theme(cls, fig, title_prefix=""):
        """Apply enhanced consistent theme to any figure"""
        fig.update_layout(
            template=cls.TEMPLATE,
            **cls.CHART_CONFIG,
            title=dict(
                text=f"{title_prefix}{fig.layout.title.text}" if fig.layout.title.text else title_prefix,
                font=dict(
                    family=cls.TYPOGRAPHY['font_family'],
                    size=16,
                    color=cls.COLORS['text']
                ),
                x=0.5,
                y=0.95
            ),
            font=dict(
                family=cls.TYPOGRAPHY['font_family'],
                size=int(cls.TYPOGRAPHY['sizes']['sm'].replace('px', '')),
                color=cls.COLORS['text']
            ),
            xaxis=dict(
                gridcolor=cls.COLORS['grid'],
                zeroline=False,
                showspikes=True,
                spikethickness=1,
                spikecolor=cls.COLORS['text'],
                spikemode='across',
                title_font=dict(size=14)
            ),
            yaxis=dict(
                gridcolor=cls.COLORS['grid'],
                zeroline=False,
                showspikes=True,
                spikethickness=1,
                spikecolor=cls.COLORS['text'],
                spikemode='across',
                title_font=dict(size=14)
            ),
            dragmode='zoom',
            hovermode='closest',
            hoverlabel=dict(
                bgcolor=cls.COLORS['background'],
                font_size=12,
                font_family="Arial, sans-serif"
            )
        )
        return fig

    @classmethod
    def get_styled_text_area(cls):
        """Returns CSS for styled text areas"""
        return f"""
        <style>
        .stTextArea textarea {{
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['text']};
            font-family: 'Arial', sans-serif;
            font-size: 14px;
            line-height: 1.5;
            padding: 15px;
            border: 1px solid {cls.COLORS['grid']};
            border-radius: 5px;
        }}
        </style>
        """

def create_transaction_amount_distribution(data, title="Transaction Amount Distribution"):
    fig = px.histogram(
        data, 
        x="amount",
        title=title,
        color_discrete_sequence=[VisualizationTheme.COLORS['primary']]
    )
    fig.update_layout(
        xaxis_title="Transaction Amount",
        yaxis_title="Frequency",
        showlegend=True,
        bargap=0.1
    )
    return VisualizationTheme.apply_theme(fig)

def create_violations_summary(rule_violations_count):
    fig = go.Figure(data=[
        go.Bar(
            x=list(rule_violations_count.keys()),
            y=list(rule_violations_count.values()),
            marker_color=VisualizationTheme.COLORS['primary']
        )
    ])
    fig.update_layout(
        title="Rule Violations Summary",
        xaxis_title="Rules",
        yaxis_title="Number of Violations",
        xaxis_tickangle=-45
    )
    return VisualizationTheme.apply_theme(fig)

def create_customer_dashboard(transactions):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Transaction Amounts", "Transaction Types", 
                       "Daily Transaction Volume", "Geographic Distribution")
    )
    
    # Add your subplots here
    # Example:
    fig.add_trace(
        go.Histogram(x=transactions['amount'], name="Amount Distribution"),
        row=1, col=1
    )
    
    fig.update_layout(
        height=800,
        showlegend=True,
        title_text="Customer Transaction Analysis Dashboard",
        title_x=0.5
    )
    return VisualizationTheme.apply_theme(fig)

def create_preview_dashboard(transactions):
    """Creates a professional dashboard for data preview"""
    # Transaction Volume Over Time
    if 'date' in transactions.columns:
        daily_volume = transactions.groupby('date').size().reset_index(name='count')
        volume_fig = px.line(
            daily_volume, 
            x='date', 
            y='count',
            title='Transaction Volume Trend'
        )
        volume_fig.update_traces(
            line_color=VisualizationTheme.COLORS['primary'],
            line_width=2,
            mode='lines+markers',
            marker=dict(size=6)
        )
    else:
        volume_fig = go.Figure()
        volume_fig.update_layout(title="Transaction Volume Trend (No date data available)")
    
    VisualizationTheme.apply_theme(volume_fig)

    # Amount Distribution with improved binning
    amount_fig = px.histogram(
        transactions,
        x="amount",
        title='Transaction Amount Distribution',
        nbins=40,
        opacity=0.75,
        color_discrete_sequence=[VisualizationTheme.COLORS['primary']]
    )
    amount_fig.update_layout(
        bargap=0.2,
        selectdirection="h"
    )
    VisualizationTheme.apply_theme(amount_fig)

    # Customer Distribution with improved styling
    customer_dist = transactions.groupby('customer_id')['amount'].sum().sort_values(ascending=True).tail(10)
    types_fig = px.bar(
        x=customer_dist.values,
        y=customer_dist.index,
        title='Top 10 Customers by Volume',
        orientation='h',
        color_discrete_sequence=[VisualizationTheme.COLORS['accent']]
    )
    types_fig.update_traces(
        width=0.7,
        opacity=0.8,
        hovertemplate="<b>Customer:</b> %{y}<br>" +
                      "<b>Amount:</b> $%{x:,.2f}<extra></extra>"
    )
    VisualizationTheme.apply_theme(types_fig)

    return volume_fig, amount_fig, types_fig

def create_summary_card(title, value, prefix="", suffix=""):
    """Creates a styled metric card"""
    return {
        "title": title,
        "value": f"{prefix}{value:,.2f}{suffix}",
        "style": {
            "background": VisualizationTheme.COLORS['background'],
            "color": "white",
            "padding": "1rem",
            "border-radius": "5px",
            "box-shadow": "0 2px 4px rgba(0,0,0,0.1)"
        }
    }

def create_summary_metrics(transactions):
    """Creates summary metrics with consistent styling"""
    return {
        "Total Transactions": create_summary_card("Total Transactions", len(transactions)),
        "Total Volume": create_summary_card("Total Volume", transactions['amount'].sum(), "$"),
        "Average Transaction": create_summary_card("Average Transaction", transactions['amount'].mean(), "$"),
        "Unique Customers": create_summary_card("Unique Customers", transactions['customer_id'].nunique())
    }
