import pandas as pd
import plotly.express as px
import plotly.io as pio

def generate_charts(data):
    charts = {}

    # Theme settings for consistent styling
    base_layout = dict(
        plot_bgcolor='#fdf6f0',
        paper_bgcolor='#fdf6f0',
        font=dict(family='Segoe UI', size=14, color='#3b2f2f'),
        title_font=dict(size=22, color='#3b2f2f'),
        hoverlabel=dict(bgcolor='white', font_size=14)
    )

    # Chart 1: Book Sales by Category (Online Only)
    df_quantity = data['category_breakdown'].copy()
    df_quantity = df_quantity.sort_values(by='total_quantity', ascending=False)
    fig1 = px.bar(
        df_quantity,
        x='category',
        y='total_quantity',
        color='category',
        title='📚 Book Sales by Category (Online Only)',
        labels={'total_quantity': 'Units Sold', 'category': 'Category'}
    )
    fig1.update_layout(base_layout)
    charts['chart1'] = pio.to_html(fig1, full_html=False)

    # ✅ Chart 2: Monthly Revenue Comparison with correct datetime
        # Chart 2: Monthly Sales Comparison (Revenue)
    df_monthly = data['comparison'].copy()

    # Convert 'month' directly to datetime (assuming it is in 'YYYY-MM' or 'YYYY-MM-DD' format)
    df_monthly['date'] = pd.to_datetime(df_monthly['month'])
    df_monthly = df_monthly.sort_values('date')

    min_date = df_monthly['date'].min().strftime('%Y-%m-%d')

    fig2 = px.line(
        df_monthly,
        x='date',
        y=['online', 'physical'],
        labels={'value': 'Revenue (DH)', 'date': 'Month'},
        title='📊 Monthly Revenue Comparison: Online vs Physical'
    )
    fig2.update_layout(
        base_layout,
        xaxis=dict(range=[min_date, None], tickformat="%b %Y")
    )
    charts['chart2'] = pio.to_html(fig2, full_html=False)

    # Chart 3: Total Revenue by Category (Online Only)
    df_revenue_cat = data['favorite_category'].copy()
    df_revenue_cat = df_revenue_cat.sort_values(by='total_revenue', ascending=False)
    fig3 = px.bar(
        df_revenue_cat,
        x='category',
        y='total_revenue',
        color='category',
        title='💰 Total Revenue by Category (Online Only)',
        labels={'total_revenue': 'Total Revenue (DH)', 'category': 'Category'}
    )
    fig3.update_layout(base_layout)
    charts['chart3'] = pio.to_html(fig3, full_html=False)


        # Chart 4: Monthly Total Items Sold and Revenue by Shop
    df_items = data['items_by_period'].copy()
    df_revenue = data['revenue_by_period'].copy()

    # Convert 'month' column directly to datetime if it already has 'YYYY-MM' or 'YYYY-MM-DD' format
    df_items['date'] = pd.to_datetime(df_items['month'])
    df_revenue['date'] = pd.to_datetime(df_revenue['month'])

    df_time = pd.merge(
        df_items[['shop', 'date', 'total_items_sold']],
        df_revenue[['shop', 'date', 'total_revenue']],
        on=['shop', 'date'],
        how='outer'
    )

    min_time = df_time['date'].min().strftime('%Y-%m-%d')

    fig4 = px.line(
        df_time.sort_values('date'),
        x='date',
        y=['total_items_sold', 'total_revenue'],
        color='shop',
        title='📈 Monthly Items Sold & Revenue by Shop',
        labels={'value': 'Total', 'date': 'Month'}
    )
    fig4.update_layout(
        base_layout,
        xaxis=dict(range=[min_time, None], tickformat="%b %Y")
    )
    charts['chart4'] = pio.to_html(fig4, full_html=False)

    # Chart 5: Top-Selling Books
    df_top_products = data['top_products'].copy()
    fig5 = px.bar(
        df_top_products.sort_values(by='total_quantity', ascending=False).head(5),
        x='product_name',
        y='total_quantity',
        title='🏆 Top 5 Selling Books by Quantity',
        labels={'product_name': 'Book Name', 'total_quantity': 'Units Sold'},
        color='product_name'
    )
    fig5.update_layout(base_layout)
    charts['chart5'] = pio.to_html(fig5, full_html=False)

    # ✅ Chart 6: Delivery Status Distribution
  

    return charts
