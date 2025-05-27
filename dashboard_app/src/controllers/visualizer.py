# dashboard_app/src/controllers/visualizer.py

import pandas as pd
import plotly.express as px
import plotly.io as pio


def generate_charts(data):
    charts = {}

    # Chart 1: Book Sales by Category and Shop Type
    df_quantity = data['category_breakdown']
    fig1 = px.bar(df_quantity, x='category', y='total_quantity', color='shop', barmode='group',
                  title='Book Sales by Category and Shop Type')
    charts['chart1'] = pio.to_html(fig1, full_html=False)

    # Chart 2: Monthly Sales Comparison
    df_monthly = data['comparison']
    fig2 = px.line(df_monthly, x='month', y=['online', 'physical'],
                   labels={'value': 'Sales', 'month': 'Month'},
                   title='Monthly Sales Comparison: Online vs Physical')
    charts['chart2'] = pio.to_html(fig2, full_html=False)

    # Chart 3: Total Revenue by Category and Shop
    df_revenue_cat = data['favorite_category']
    fig3 = px.bar(df_revenue_cat, x='category', y='total_revenue', color='shop',
                  title='Total Revenue by Category and Shop Type')
    charts['chart3'] = pio.to_html(fig3, full_html=False)

    # Chart 4: Daily Online Sales & Revenue
    df_items = data['items_by_period']
    df_revenue_day = data['revenue_by_period']

    df_items['day'] = pd.to_datetime(df_items['day'])
    df_revenue_day['day'] = pd.to_datetime(df_revenue_day['day'])

    df_time = pd.merge(df_items, df_revenue_day[['day', 'total_revenue']], on='day', how='outer')
    fig4 = px.line(df_time.sort_values('day'), x='day', y=['total_items_sold', 'total_revenue'],
                   title='Daily Online Sales & Revenue',
                   labels={'value': 'Total', 'day': 'Date'})
    charts['chart4'] = pio.to_html(fig4, full_html=False)

    # Chart 5: Top-Selling Books
    df_top_products = data['top_products']
    fig5 = px.bar(df_top_products, x='product_name', y='total_quantity',
                  title='Top-Selling Books by Quantity')
    charts['chart5'] = pio.to_html(fig5, full_html=False)

    return charts
