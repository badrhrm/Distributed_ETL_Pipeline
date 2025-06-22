import pandas as pd
import os

# Function to clean data using data_dictionary
def load_and_clean_data(data_dictionary):
    # Extract dataframes from dictionary
    books_df = data_dictionary['books']
    authors_df = data_dictionary['authors']
    orders_df = data_dictionary['orders']
    order_items_df = data_dictionary['order_items']
    users_df = data_dictionary['users']
    physical_sales_df = data_dictionary['physical_shop_sales']

    # Clean order_items data
    order_items_df = order_items_df.dropna(subset=['order_id', 'book_id', 'quantity', 'price_at_order'])
    order_items_df['quantity'] = pd.to_numeric(order_items_df['quantity'], errors='coerce')
    order_items_df['price_at_order'] = pd.to_numeric(order_items_df['price_at_order'], errors='coerce')

    # Prepare books data
    books_df = books_df.rename(columns={'name': 'book_name'})
    order_items_df = order_items_df.merge(books_df[['book_id', 'book_name', 'category']], on='book_id', how='left')

    # Merge with orders
    orders_df['order_date'] = pd.to_datetime(orders_df['order_date'], errors='coerce')
    order_items_df = order_items_df.merge(orders_df[['order_id', 'order_date', 'user_id']], on='order_id', how='left')

    # Merge with users (optional gender info)
    if 'gender' in users_df.columns:
        order_items_df = order_items_df.merge(users_df[['user_id', 'gender']], on='user_id', how='left')
    else:
        order_items_df['gender'] = 'Unknown'

    # Finalize online data
    order_items_df['date'] = order_items_df['order_date']
    order_items_df['price'] = order_items_df['price_at_order']
    order_items_df['shop'] = 'online'
    order_items_df['product_name'] = order_items_df['book_name']
    order_items_df = order_items_df[['date', 'product_name', 'category', 'quantity', 'price', 'shop', 'gender']]
    order_items_df = order_items_df.dropna(subset=['date'])

    # Clean physical shop data
    physical_sales_df = physical_sales_df.dropna(subset=['Date', 'Book Title', 'Quantity', 'Unit Price'])
    physical_sales_df['quantity'] = pd.to_numeric(physical_sales_df['Quantity'], errors='coerce')
    physical_sales_df['price'] = pd.to_numeric(physical_sales_df['Unit Price'], errors='coerce')
    physical_sales_df['date'] = pd.to_datetime(physical_sales_df['Date'], errors='coerce')
    physical_sales_df = physical_sales_df.rename(columns={
        'Book Title': 'product_name'
    })
    physical_sales_df['shop'] = 'physical'
    physical_sales_df['gender'] = 'Unknown'
    physical_sales_df['category'] = 'Unknown'  # Set default if missing
    physical_sales_df = physical_sales_df[['date', 'product_name', 'category', 'quantity', 'price', 'shop', 'gender']]
    physical_sales_df = physical_sales_df.dropna(subset=['date'])

    return order_items_df, physical_sales_df


# Transform and analyze
def transform_all_data(online_df, physical_df):
    combined_df = pd.concat([online_df, physical_df], ignore_index=True)

    combined_df['quantity'] = combined_df['quantity'].fillna(0)
    combined_df['price'] = combined_df['price'].fillna(0)
    combined_df['revenue'] = combined_df['quantity'] * combined_df['price']
    combined_df['year'] = combined_df['date'].dt.year
    combined_df['month'] = combined_df['date'].dt.month
    combined_df['week'] = combined_df['date'].dt.isocalendar().week
    combined_df['day'] = combined_df['date'].dt.date

    items_by_period = combined_df.groupby(['shop', 'year', 'month'])['quantity'].sum().reset_index(name='total_items_sold')
    revenue_by_period = combined_df.groupby(['shop', 'year', 'month'])['revenue'].sum().reset_index(name='total_revenue')
    category_breakdown = online_df.groupby(['category'])['quantity'].sum().reset_index(name='total_quantity')

    top_products = combined_df.groupby('product_name')['quantity'].sum().reset_index(name='total_quantity') \
                              .sort_values(by='total_quantity', ascending=False).head(5)

    monthly_stats = combined_df.groupby(['shop', 'month']).agg({'quantity': 'sum', 'revenue': 'sum'}).reset_index()
    comparison_df = monthly_stats.pivot(index='month', columns='shop', values='revenue').reset_index()
    comparison_df['difference'] = comparison_df.get('online', 0) - comparison_df.get('physical', 0)
    comparison_df['trend'] = comparison_df['difference'].apply(lambda x: '📈 Improved' if x > 0 else '📉 Declined')

    online_df = combined_df[combined_df['shop'] == 'online']
    gender_category = online_df.groupby(['gender', 'category']).agg({'quantity': 'sum'}).reset_index()
    gender_comparison = gender_category.loc[gender_category.groupby('gender')['quantity'].idxmax()]

    favorite_category = online_df.groupby(['category'])['revenue'].sum().reset_index(name='total_revenue') \
                                   .sort_values(by='total_revenue', ascending=False)

    return {
        "combined": combined_df,
        "items_by_period": items_by_period,
        "revenue_by_period": revenue_by_period,
        "category_breakdown": category_breakdown,
        "top_products": top_products,
        "comparison": comparison_df,
        "gender_comparison": gender_comparison,
        "favorite_category": favorite_category
    }


# Save results
def save_results(results, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    results['combined'].to_csv(f"{output_dir}/combined.csv", index=False)
    results['items_by_period'].to_csv(f"{output_dir}/items_by_period.csv", index=False)
    results['revenue_by_period'].to_csv(f"{output_dir}/revenue_by_period.csv", index=False)
    results['category_breakdown'].to_csv(f"{output_dir}/category_breakdown.csv", index=False)
    results['top_products'].to_csv(f"{output_dir}/top_products.csv", index=False)
    results['comparison'].to_csv(f"{output_dir}/comparison.csv", index=False)
    results['gender_comparison'].to_csv(f"{output_dir}/gender_comparison.csv", index=False)
    results['favorite_category'].to_csv(f"{output_dir}/favorite_category.csv", index=False)
    print(f"All analysis results saved in: {output_dir}")


# Run pipeline
def run_pipeline(data_dictionary):
    print("Loading and cleaning data...")
    online_df, physical_df = load_and_clean_data(data_dictionary)

    print("Transforming and analyzing...")
    results = transform_all_data(online_df, physical_df)

    print("Saving results...")
    save_results(results)

# To use: pass your data_dictionary to run_pipeline
# run_pipeline(data_dictionary)