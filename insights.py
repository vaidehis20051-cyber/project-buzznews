import pymysql

def get_db_connection():
    """Return a pymysql connection with DictCursor."""
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='buzznews',
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )


def get_user_stats():
    """Return counts of users by role (User / Moderator / Journalist)."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT r.name AS role_name, COUNT(u.id) AS total
        FROM users u
        JOIN roles r ON u.role_id = r.id
        GROUP BY r.name
    """)
    rows = cursor.fetchall()
    connection.close()
    return {row['role_name']: row['total'] for row in rows}


def get_todays_articles():
    """
    Return a list of dicts of today's articles grouped by status:
    [{'status': 'pending', 'count': 5}, ...]
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT status, COUNT(*) AS count
        FROM articles
        WHERE DATE(submit_time) = CURDATE()
        GROUP BY status
    """)
    rows = cursor.fetchall()
    connection.close()
    return rows


def get_review_panel_counts():
    """
    Return counts of normal and local voice articles grouped by status:
    {'articles_pending': 2, 'articles_approved': 5, 'local_pending': 1, ...}
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    review_panel = {
        "articles_pending": 0,
        "articles_approved": 0,
        "articles_rejected": 0,
        "local_pending": 0,
        "local_approved": 0,
        "local_rejected": 0
    }

    # Normal articles
    cursor.execute("""
        SELECT status, COUNT(*) AS total
        FROM articles
        WHERE is_local_voice = 0
        GROUP BY status
    """)
    for row in cursor.fetchall():
        review_panel[f"articles_{row['status']}"] = row['total']

    # Local voice articles
    cursor.execute("""
        SELECT status, COUNT(*) AS total
        FROM articles
        WHERE is_local_voice = 1
        GROUP BY status
    """)
    for row in cursor.fetchall():
        review_panel[f"local_{row['status']}"] = row['total']

    cursor.close()
    connection.close()
    return review_panel


def get_website_stats():
    """Return total articles, total users, active authors in last 30 days."""
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) AS total_articles FROM articles")
    total_articles = cursor.fetchone()['total_articles']

    cursor.execute("SELECT COUNT(*) AS total_users FROM users")
    total_users = cursor.fetchone()['total_users']

    cursor.execute("""
        SELECT COUNT(DISTINCT author_id) AS active_authors
        FROM articles
        WHERE DATE(submit_time) >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    """)
    active_authors = cursor.fetchone()['active_authors']

    connection.close()

    return {
        'total_articles': total_articles,
        'total_users': total_users,
        'active_authors': active_authors
    }
