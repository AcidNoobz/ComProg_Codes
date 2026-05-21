from db import cursor, conn
import matplotlib.pyplot as plt
from datetime import datetime

# overall sales
def total_sales():

    cursor.execute("SELECT total FROM sales")

    records = cursor.fetchall()

    overall = 0

    for row in records:
        overall += row[0]

    return overall


# daily sales
def daily_sales():

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
    SELECT SUM(total)
    FROM sales
    WHERE date = ?
    """, (today,))

    result = cursor.fetchone()[0]

    if result is None:
        result = 0

    return result


# weekly sales
def weekly_sales():

    cursor.execute("SELECT total FROM sales")

    records = cursor.fetchall()

    weekly = 0

    for row in records:
        weekly += row[0]

    return weekly


# monthly sales
def monthly_sales():

    month = datetime.now().strftime("%Y-%m")

    cursor.execute("""
    SELECT SUM(total)
    FROM sales
    WHERE date LIKE ?
    """, (month + "%",))

    result = cursor.fetchone()[0]

    if result is None:
        result = 0

    return result


# yearly sales
def yearly_sales():

    year = datetime.now().strftime("%Y")

    cursor.execute("""
    SELECT SUM(total)
    FROM sales
    WHERE date LIKE ?
    """, (year + "%",))

    result = cursor.fetchone()[0]

    if result is None:
        result = 0

    return result


# sales chart
def sales_chart():

    cursor.execute("""
    SELECT product_name, total
    FROM sales
    """)

    data = cursor.fetchall()

    products = []
    totals = []

    for row in data:
        products.append(row[0])
        totals.append(row[1])

    plt.bar(products, totals)
    plt.xticks(rotation=40, ha="right", fontsize=10)

    plt.title("Luis Bakery Sales")

    plt.xlabel("Products")

    plt.ylabel("Sales")

    plt.tight_layout()
    plt.show()