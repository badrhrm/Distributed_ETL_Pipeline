from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.models.user import User
from src.controllers.auth import login_user, logout_user, get_current_user
from src.controllers.orchestration_controller import trigger_etl_process
from src.controllers.schedule_controller import update_schedule
#from loading_logic import get_loaded_data  # 🔁 Assure-toi que le chemin est correct
import sys
import os
from flask import render_template
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from loading_service.loading_logic import get_loaded_data
import pandas as pd
import plotly.express as px
import plotly.io as pio
# 👇 This adds the root directory (dashboard_app) to sys.path

import pandas as pd
import plotly.express as px
import plotly.io as pio

main = Blueprint('main', __name__)

@main.route('/')
def home():
    username = get_current_user()
    if username:
        return render_template('home.html', username=username)
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.authenticate(username, password)
        if user:
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/trigger_etl', methods=['POST'])
def trigger_etl():
    message = trigger_etl_process()
    return render_template('home.html', message=message)

@main.route('/schedule', methods=['GET', 'POST'])
def update_schedule_view():
    if request.method == 'POST':
        return update_schedule()
    return render_template('set_schedule.html')


@main.route('/visualize')
def visualize():
    data = get_loaded_data()

    if not data:
        return render_template('visualize.html', error="❌ No data loaded. Please trigger ETL first.")

    try:
        # --- Chart 1: Category Quantity ---
        df_quantity = data['category_breakdown']
        fig1 = px.bar(df_quantity, x='category', y='total_quantity', color='shop', barmode='group',
                      title='Book Sales by Category and Shop Type')
        chart1 = pio.to_html(fig1, full_html=False)

        # --- Chart 2: Monthly Sales Trend ---
        df_monthly = data['comparison']
        fig2 = px.line(df_monthly, x='month', y=['online', 'physical'],
                       labels={'value': 'Sales', 'month': 'Month'},
                       title='Monthly Sales Comparison: Online vs Physical')
        chart2 = pio.to_html(fig2, full_html=False)

        # --- Chart 3: Revenue by Category ---
        df_revenue_cat = data['favorite_category']
        fig3 = px.bar(df_revenue_cat, x='category', y='total_revenue', color='shop',
                      title='Total Revenue by Category and Shop Type')
        chart3 = pio.to_html(fig3, full_html=False)

        # --- Chart 4: Daily Sales and Revenue ---
        df_items = data['items_by_period']
        df_revenue_day = data['revenue_by_period']

        df_items['day'] = pd.to_datetime(df_items['day'])
        df_revenue_day['day'] = pd.to_datetime(df_revenue_day['day'])

        df_time = pd.merge(df_items, df_revenue_day[['day', 'total_revenue']], on='day', how='outer')
        fig4 = px.line(df_time.sort_values('day'), x='day', y=['total_items_sold', 'total_revenue'],
                       title='Daily Online Sales & Revenue',
                       labels={'value': 'Total', 'day': 'Date'})
        chart4 = pio.to_html(fig4, full_html=False)

        # --- Chart 5: Top-Selling Products ---
        df_top_products = data['top_products']
        fig5 = px.bar(df_top_products, x='product_name', y='total_quantity',
                      title='Top-Selling Books by Quantity')
        chart5 = pio.to_html(fig5, full_html=False)

        return render_template('visualize.html',
                               chart1=chart1, chart2=chart2, chart3=chart3,
                               chart4=chart4, chart5=chart5)

    except Exception as e:
        return render_template('visualize.html', error=f"❌ Error rendering charts: {e}")
