from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, to_date, year, month, weekofyear, date_format,
    sum as _sum, lit, expr, row_number
)
from pyspark.sql.window import Window
import os

def load_and_clean_data(data_dictionary):
    books_df = data_dictionary['books']
    orders_df = data_dictionary['orders']
    order_items_df = data_dictionary['order_items']
    users_df = data_dictionary['users']
    physical_sales_df = data_dictionary['physical_shop_sales']

    # Clean order_items
    order_items_df = order_items_df.dropna(subset=['order_id', 'book_id', 'quantity', 'price_at_order']) \
        .withColumn('quantity', col('quantity').cast('double')) \
        .withColumn('price_at_order', col('price_at_order').cast('double'))

    # Prepare books
    books_df = books_df.withColumnRenamed('name', 'book_name')
    order_items_df = order_items_df.join(books_df.select('book_id', 'book_name', 'category'), on='book_id', how='left')

    # Join orders
    orders_df = orders_df.withColumn('order_date', to_date(col('order_date')))
    order_items_df = order_items_df.join(orders_df.select('order_id', 'order_date', 'user_id'), on='order_id', how='left')

    # Join users
    if 'gender' in users_df.columns:
        order_items_df = order_items_df.join(users_df.select('user_id', 'gender'), on='user_id', how='left')
    else:
        order_items_df = order_items_df.withColumn('gender', lit('Unknown'))

    # Finalize online sales
    online_df = order_items_df.withColumnRenamed('order_date', 'date') \
        .withColumn('price', col('price_at_order')) \
        .withColumn('shop', lit('online')) \
        .withColumnRenamed('book_name', 'product_name') \
        .select('date', 'product_name', 'category', 'quantity', 'price', 'shop', 'gender') \
        .dropna(subset=['date'])

    # Clean physical shop sales
    physical_df = physical_sales_df.dropna(subset=['Date', 'Book Title', 'Quantity', 'Unit Price']) \
        .withColumn('date', to_date(col('Date'))) \
        .withColumn('quantity', col('Quantity').cast('double')) \
        .withColumn('price', col('Unit Price').cast('double')) \
        .withColumn('product_name', col('Book Title')) \
        .withColumn('category', lit('Unknown')) \
        .withColumn('shop', lit('physical')) \
        .withColumn('gender', lit('Unknown')) \
        .select('date', 'product_name', 'category', 'quantity', 'price', 'shop', 'gender') \
        .dropna(subset=['date'])

    return online_df, physical_df


def transform_and_analyze(online_df, physical_df):
    combined_df = online_df.unionByName(physical_df)

    combined_df = combined_df.fillna({'quantity': 0, 'price': 0})
    combined_df = combined_df.withColumn('revenue', col('quantity') * col('price')) \
                             .withColumn('year', year('date')) \
                             .withColumn('month', month('date')) \
                             .withColumn('week', weekofyear('date')) \
                             .withColumn('day', date_format('date', 'yyyy-MM-dd'))

    items_by_period = combined_df.groupBy('shop', 'year', 'month', 'week', 'day') \
                                 .agg(_sum('quantity').alias('total_items_sold'))

    revenue_by_period = combined_df.groupBy('shop', 'year', 'month', 'week', 'day') \
                                   .agg(_sum('revenue').alias('total_revenue'))

    category_breakdown = combined_df.groupBy('shop', 'category') \
                                    .agg(_sum('quantity').alias('total_quantity'))

    top_products = combined_df.groupBy('product_name') \
                              .agg(_sum('quantity').alias('total_quantity')) \
                              .orderBy(col('total_quantity').desc()) \
                              .limit(5)

    monthly_stats = combined_df.groupBy('shop', 'month') \
                               .agg(_sum('quantity').alias('quantity'), _sum('revenue').alias('revenue'))

    comparison_df = monthly_stats.groupBy('month').pivot('shop').sum('revenue') \
        .fillna(0) \
        .withColumn('difference', col('online') - col('physical')) \
        .withColumn('trend', when(col('difference') > 0, '📈 Improved').otherwise('📉 Declined'))

    online_only = combined_df.filter(col('shop') == 'online')
    gender_category = online_only.groupBy('gender', 'category') \
                                 .agg(_sum('quantity').alias('quantity'))

    window = Window.partitionBy('gender').orderBy(col('quantity').desc())
    gender_comparison = gender_category.withColumn('rank', row_number().over(window)) \
                                       .filter(col('rank') == 1).drop('rank')

    favorite_category = combined_df.groupBy('shop', 'category') \
                                   .agg(_sum('revenue').alias('total_revenue')) \
                                   .orderBy(col('total_revenue').desc())

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


def save_results(results, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    for key, df in results.items():
        df.write.mode("overwrite").option("header", "true").csv(f"{output_dir}/{key}")
    print(f"✅ All Spark analysis results saved to CSVs in: {output_dir}")


def run_pipeline(data_dictionary):
    print("🔄 Loading and cleaning data...")
    online_df, physical_df = load_and_clean_data(data_dictionary)

    print("⚙️  Transforming and analyzing...")
    results = transform_and_analyze(online_df, physical_df)

    print("💾 Saving results...")
    save_results(results)
