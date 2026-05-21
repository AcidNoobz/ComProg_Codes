from db import cursor, conn

# =========================
# ADD SALE
# =========================

def add_sale(product, category, quantity, price, date):

    total = quantity * price

    cursor.execute("""
    INSERT INTO sales
    (product_name, category, quantity, price, total, date)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (product, category, quantity, price, total, date))

    conn.commit()


# =========================
# GET ALL SALES
# =========================

def get_sales():

    cursor.execute("""
    SELECT * FROM sales
    """)

    return cursor.fetchall()


# =========================
# DELETE SALE
# =========================

def delete_sale(id):

    cursor.execute("""
    DELETE FROM sales
    WHERE id = ?
    """, (id,))

    conn.commit()


# =========================
# SEARCH PRODUCT
# =========================

def search_sale(keyword):

    cursor.execute("""
    SELECT * FROM sales
    WHERE product_name LIKE ?
    """, ('%' + keyword + '%',))

    return cursor.fetchall()


# =========================
# UPDATE SALE
# =========================

def update_sale(id, product, category, quantity, price, date):

    total = quantity * price

    cursor.execute("""
    UPDATE sales
    SET
        product_name = ?,
        category = ?,
        quantity = ?,
        price = ?,
        total = ?,
        date = ?
    WHERE id = ?
    """,
    (product, category, quantity, price, total, date, id))

    conn.commit()


# =========================
# FILTER CATEGORY
# =========================

def filter_category(category):

    cursor.execute("""
    SELECT * FROM sales
    WHERE category = ?
    """, (category,))

    return cursor.fetchall()


# =========================
# SORT BY CATEGORY

def sort_by_category():

    cursor.execute("""
    SELECT * FROM sales
    ORDER BY LOWER(category) ASC
    """)

    return cursor.fetchall()


# =========================
# SORT BY DATE
# =========================

def sort_by_date():

    cursor.execute("""
    SELECT * FROM sales
    ORDER BY date DESC
    """)

    return cursor.fetchall()


# =========================
# SORT BY TOTAL SALES
# =========================

def sort_by_total():

    cursor.execute("""
    SELECT * FROM sales
    ORDER BY total DESC
    """)

    return cursor.fetchall()