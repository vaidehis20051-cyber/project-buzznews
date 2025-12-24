from flask import Flask, request, session, flash, redirect, url_for, render_template,jsonify
from sqlalchemy import all_
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os, base64,re
from PIL import Image
import time

from insights import (
    get_user_stats,
    get_todays_articles,
    get_review_panel_counts,
    get_website_stats
)

pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.secret_key = "buzznews"  

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/buzznews'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS


# ------------------- MODELS -------------------
class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Districts(db.Model):
    __tablename__ = 'districts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'), nullable=True)
    role = db.relationship('Roles', backref='users')
    district = db.relationship('Districts', backref='users')

# ------------------- DB CONNECTION -------------------
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='buzznews',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

# ------------------- IMAGE UPLOAD SETTINGS -------------------
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_image(file):
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        img = Image.open(file)
        img.thumbnail((1200, 1200))
        img.save(path, optimize=True, quality=70)
        return filename
    except Exception as e:
        print(f"Error saving image: {e}")
        return None

# ------------------- DB SETUP -------------------
def run_db_setup():
    """Executes SQL commands from db_setup.sql to initialize the database."""
    setup_file = os.path.join(os.path.dirname(__file__), 'db_setup.sql')
    if not os.path.exists(setup_file):
        print("[WARNING] db_setup.sql not found, skipping DB setup.")
        return

    try:
        with open(setup_file, 'r') as file:
            sql_commands = file.read().split(';')
    except Exception as e:
        print(f"[ERROR] Failed to read db_setup.sql: {e}")
        return

    try:
        with pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='buzznews',
            autocommit=True
        ) as connection:
            with connection.cursor() as cursor:
                for command in sql_commands:
                    cmd = command.strip()
                    if cmd and not cmd.startswith('--'):  
                        try:
                            cursor.execute(cmd)
                        except Exception as e:
                            print(f"[ERROR] Failed SQL command: {cmd}\n{e}")
                print("[INFO] DB setup completed successfully.")
    except Exception as e:
        print(f"[ERROR] Could not connect to the database: {e}")


@app.before_request
def make_session_permanent():
    session.permanent = True
# ------------------- FRONTEND ROUTES -------------------
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/buzznews/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        district_id = request.form['district_id']

        user_exists = Users.query.filter_by(username=username).first()
        if user_exists:
            flash("Username already exists. Try logging in or choose another!", 'warning')
            return redirect(url_for('user_register'))

        new_user = Users(
            username=username,
            password=password,
            role_id=4,  # reader
            district_id=int(district_id)
        )
        db.session.add(new_user)
        db.session.commit()

        flash('User registered successfully! You may login now!', 'success')
        return redirect(url_for('user_login'))

    districts = Districts.query.all()
    return render_template('user_register.html', districts=districts)


@app.route('/buzznews/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username=username, password=password).first()
        if user and user.role.name == 'reader':
            session.permanent = True
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role.name
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('user_login'))

    return render_template('user_login.html')


@app.route('/home', methods=['GET','POST'])
def home():
    if 'user_id' not in session:
        return redirect(url_for('user_login'))

    user_id = session.get("user_id")
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM notifications
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))
    all_notifications = cursor.fetchall()
    top_notifications = all_notifications[:3]

    district_id = request.args.get("district_id")
    category_id = request.args.get("category_id")
    search_query = request.args.get("search_query")

    filters_applied = bool(district_id or category_id or search_query)

    # ARTICLES  
    article_query = "SELECT * FROM articles WHERE is_local_voice = 0 AND status = 'approved'"
    article_params = []

    if district_id and district_id.strip(): 
        article_query += " AND district_id = %s" 
        article_params.append(district_id)

    if category_id and category_id.strip():
        article_query += " AND category_id = %s"
        article_params.append(category_id)

    if search_query and search_query.strip():
        article_query += " AND (title LIKE %s OR content LIKE %s)" 
        like_pattern = f"%{search_query}%" 
        article_params.extend([like_pattern, like_pattern])
    
    article_query += " ORDER BY submit_time DESC LIMIT 20"
    
    cursor.execute(article_query, tuple(article_params))
    articles = cursor.fetchall()

    # ---------- LOCAL VOICES ----------
    lv_query = "SELECT * FROM articles WHERE is_local_voice = 1 AND status = 'approved'"
    lv_params = []

    if district_id and district_id.strip():
        lv_query += " AND district_id = %s"
        lv_params.append(district_id)

    if category_id and category_id.strip():
        lv_query += " AND category_id = %s"
        lv_params.append(category_id)

    if search_query and search_query.strip():
        lv_query += " AND (title LIKE %s OR content LIKE %s)"
        like_pattern = f"%{search_query}%"
        lv_params.extend([like_pattern, like_pattern])

    lv_query += " ORDER BY submit_time DESC LIMIT 6"
    cursor.execute(lv_query, tuple(lv_params))
    local_voices = cursor.fetchall()

    # ---------- DROPDOWNS ----------
    cursor.execute("SELECT id, name FROM districts ORDER BY name")
    districts = cursor.fetchall()
    
    cursor.execute("SELECT id, name FROM categories ORDER BY name")
    categories = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "home.html",
        user=user,
        articles=articles,
        local_voices=local_voices,
        districts=districts,
        categories=categories,
        selected_district=district_id,
        selected_category=category_id,
        search_query=search_query or "",
        filters_applied=filters_applied,
        notifications = top_notifications,
        all_notifications=all_notifications
    )


# ------------------- PROFILE -------------------
@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    user_id = session.get("user_id")
    if not user_id:
        flash("Login required", "danger")
        return redirect(url_for("user_login"))

    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if request.method == 'POST':
        updates, params = [], []
        next_page = request.form.get("next") 

        username = request.form.get("username")
        current_password = request.form.get("password")
        bio = request.form.get("bio")
        profile_image = request.files.get("profile_image")
        current_profile_image = request.form.get("current_profile_image")
        if not current_profile_image or current_profile_image.lower() == 'undefined':
            current_profile_image = None
        
        # Profile Image
        if profile_image and profile_image.filename:
            filename = secure_filename(profile_image.filename)
            profile_path = os.path.join("static/uploads", filename)
            profile_image.save(profile_path)
            updates.append("profile_image=%s")
            params.append(filename)
        else:
            updates.append("profile_image=%s")
            params.append(current_profile_image if current_profile_image else None)

        # Username & password & bio
        if user['role_id'] in [2,3]:
            username = user['username']  
        if username: 
            updates.append("username=%s")
            params.append(username)
        current_password_input = request.form.get("current_password")
        new_password = request.form.get("new_password")

        if current_password_input and new_password:
            if current_password_input == user['password']:  
                updates.append("password=%s")
                params.append(new_password)
            else:
                flash("Current password is incorrect. Password not changed.", "danger")
        if bio:
            updates.append("bio=%s")
            params.append(bio)

        if updates:
            query = f"UPDATE users SET {', '.join(updates)} WHERE id=%s"
            params.append(user_id)
            cursor.execute(query, params)
            connection.commit()
            
            cursor.execute("SELECT username, password, bio, profile_image FROM users WHERE id=%s", (user_id,))
            updated_user = cursor.fetchone()
            if updated_user:
                session['username'] = updated_user['username']
                session['password'] = updated_user['password']
            flash("Profile updated successfully!", "success")
            if next_page:
                return redirect(next_page)

    cursor.close()
    connection.close()
    return render_template("home.html", user=user)


# ------------------- PERSONNEL LOGIN -------------------
@app.route('/buzznews/personnel', methods=['GET', 'POST'])
def personnel_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username, password=password).first()
        if user and user.role.name in ['admin', 'moderator', 'journalist']:
            session.update({
                'user_id': user.id,
                'username': user.username,
                'role': user.role.name
            })
            session.permanent = True
            if user.role.name == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role.name == 'moderator':
                return redirect(url_for('moderator_dashboard'))
            elif user.role.name == 'journalist':
                return redirect(url_for('journalist_dashboard'))
        else:
            flash("Invalid credentials!", 'danger')
    return render_template('personnel_login.html')

# ------------------- ADMIN -------------------
@app.route('/personnel/admin', methods=['GET'])
def admin_dashboard():
    if session.get('role') != 'admin':
        flash("Access denied.", "danger")
        return redirect(url_for('personnel_login'))

    # Fetch data
    user_stats_dict = get_user_stats()            
    article_sitemap_list = get_todays_articles() 
    review_panel_dict = get_review_panel_counts()
    website_stats = get_website_stats()  

    user_stats = [{"role_name": k, "total": v} for k, v in user_stats_dict.items()]
    review_panel = [{"status": k, "count": v} for k, v in review_panel_dict.items()]

    # Fetch current user & districts
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    districts = Districts.query.all()

    return render_template(
        "admin_dashboard.html",
        districts=districts,
        user=user,
        user_stats=user_stats,
        article_sitemap=article_sitemap_list,
        review_panel=review_panel,
        website_stats=website_stats
    )

@app.route('/admin/add_user', methods=['POST','GET'])
def add_user():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('personnel_login'))
    
    username = request.form['username']
    password = request.form['password']
    role_id = request.form['role_id']
    district_id = request.form['district_id']
    next_page = request.form.get('next')

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, password, role_id, district_id) VALUES (%s,%s,%s,%s)",
                   (username, password, role_id, district_id))
                connection.commit()
                flash("User added successfully!", "success")
    except Exception as e:
        flash(f"Error adding user: {str(e)}", "danger")
    return redirect(next_page or url_for('admin_dashboard'))


# ------------------- JOURNALIST -------------------
@app.route('/personnel/journalist', methods=['GET', 'POST'])
def journalist_dashboard():
    if session.get('role') != 'journalist':
        flash("Access denied.", "danger")
        return redirect(url_for('personnel_login'))

    user_id = session.get("user_id")
        
    with get_db_connection() as connection:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            
            cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
            user = cursor.fetchone()

            statuses = ['draft', 'pending', 'approved', 'rejected']
            articles = {}
            for status in statuses:
                cursor.execute(
                    "SELECT * FROM articles WHERE author_id=%s AND status=%s ORDER BY submit_time DESC",
                    (user_id, status)
                )
                articles[status] = cursor.fetchall()
            cursor.execute(
                "SELECT * FROM notifications WHERE user_id=%s ORDER BY created_at DESC",
                (user_id,)
            )
            all_notifications = cursor.fetchall()
            top_notifications = all_notifications[:3]

    tab = request.args.get('tab', 'draft')
    
    return render_template('journalist_dashboard.html', user=user, articles=articles, active_tab=tab,notifications=top_notifications,
                           all_notifications=all_notifications)

# ------------------- CREATE ARTICLE -------------------
@app.route('/article', methods=['POST', 'GET'])
def create_article():
    role = session.get('role')
    if role not in ['journalist', 'admin', 'reader']:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('index'))

    user_id = session.get('user_id')
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Get next auto-increment ID for display
    cursor.execute("""
        SELECT AUTO_INCREMENT 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA='buzznews' AND TABLE_NAME='articles'
    """)
    row = cursor.fetchone()
    next_id = row['AUTO_INCREMENT'] if row and 'AUTO_INCREMENT' in row else None

    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()
    cursor.execute("SELECT id, name FROM districts")
    districts = cursor.fetchall()

    cursor.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    user = cursor.fetchone()
    
    cursor.execute("""
        SELECT id, title
        FROM articles
        WHERE author_id=%s AND status='draft'
        ORDER BY submit_time DESC
    """, (user_id,))
    drafts = cursor.fetchall()
    
    draft_id = request.args.get('draft_id')
    article_to_edit = None
    if draft_id:
        cursor.execute("""
            SELECT *
            FROM articles
            WHERE id=%s AND author_id=%s AND status='draft'
        """, (draft_id, user_id))
        article_to_edit = cursor.fetchone()

    if request.method == 'POST':
        title = (request.form.get('title') or '').strip()
        content_html = (request.form.get('content') or '').strip()
        image_url = request.files.get('image_url')
        category_id = request.form.get('category_id')
        district_id = request.form.get('district_id')
        second_district_id = request.form.get('second_district_id')
        action = request.form.get('action')
        author_id = user_id
        
        if not district_id or district_id.strip() == '':
            district_id = None
        else:
            district_id = int(district_id)

        if not second_district_id or second_district_id.strip() == '':
            second_district_id = None
        else:
            second_district_id = int(second_district_id)

        print("Action received:", action)

        if not content_html or len(re.sub(r'<[^>]*?>', '', content_html).strip()) == 0:
            flash("Content is required.", "danger")
            return redirect(request.url)
        
        if image_url and allowed_file(image_url.filename):
            filename = save_image(image_url)
            image_url = filename
        else:
            image_url = None
                       

        if role == 'admin':
            is_local_voice = 1 if 'is_local_voice' in request.form else 0
            if action == 'publish':
                status = 'approved'
            elif action == 'draft':
                status = 'draft'
            else:
                status = 'draft'
        elif role == 'journalist':
            is_local_voice = 1 if 'is_local_voice' in request.form else 0
            if action == 'publish':
                status = 'pending'
            elif action == 'draft':
                status = 'draft'
            else:
                status = 'pending'
        else:
            is_local_voice = 1
            if action == 'draft':
                status = 'draft'
            elif action == 'publish':
                status = 'pending'
            else: 
                status = 'pending'
                
        if district_id is not None:
            cursor.execute("SELECT COUNT(*) AS cnt FROM districts WHERE id = %s", (district_id,))
            result = cursor.fetchone()
            if not result or result['cnt'] == 0:
                flash("Invalid primary district selected.", "danger")
                return redirect(request.url)

        if second_district_id is not None:
            cursor.execute("SELECT COUNT(*) AS cnt FROM districts WHERE id = %s", (second_district_id,))
            result = cursor.fetchone()
            if not result or result['cnt'] == 0:
                flash("Invalid secondary district selected.", "danger")
                return redirect(request.url)


        # ---------- Insert article into database ----------
        try:
            if article_to_edit:
                cursor.execute("""
                    UPDATE articles 
                    SET title=%s, content=%s, image_url=%s, category_id=%s,
                        district_id=%s, second_district_id=%s, is_local_voice=%s, status=%s
                    WHERE id=%s AND author_id=%s
                """, (title, content_html, image_url, category_id, district_id, second_district_id,
                      is_local_voice, status, article_to_edit['id'], user_id))
            else:
                sql = """INSERT INTO articles 
                     (title, content, image_url, author_id, category_id, district_id, second_district_id, is_local_voice, status)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (title, content_html,image_url, author_id, category_id, district_id, second_district_id, is_local_voice, status))
            connection.commit()

            flash(f"Article {'saved as draft' if status=='draft' else 'submitted'}!", "success")
            if status == 'draft':
                return redirect(url_for('create_article'))
            elif role=='admin':
                return redirect(url_for('admin_dashboard'))
            elif role=='journalist':
                return redirect(url_for('journalist_dashboard'))
            else:
                return redirect(url_for('home'))

        except Exception as e:
            connection.rollback()
            flash(f"Database error: {str(e)}", "danger")
            return redirect(request.url)

    cursor.close()
    connection.close()
    return render_template('create_article.html', next_id=next_id, categories=categories, districts=districts, role=role, 
                           user=user,drafts=drafts, article_to_edit=article_to_edit)

# ------------------- VIEW ARTICLE -------------------
@app.route('/article/<int:article_id>')
def view_article(article_id):
    with get_db_connection() as connection:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT a.id, a.title, a.content, a.image_url, a.is_local_voice, a.submit_time,
                   u.username AS author,
                   c.name AS category_name,
                   d1.name AS main_district_name,
                   d2.name AS second_district_name
            FROM articles a
            JOIN users u ON a.author_id = u.id
            LEFT JOIN categories c ON a.category_id = c.id
            LEFT JOIN districts d1 ON a.district_id = d1.id
            LEFT JOIN districts d2 ON a.second_district_id = d2.id
            WHERE a.id = %s
            AND a.status = 'approved'""" 
            cursor.execute(query, (article_id,))
            article = cursor.fetchone()

    if not article:
        flash("Article not found.", "danger")
        return redirect(url_for('home'))
    next_page = request.args.get('next', 'home')
    return render_template("view_article.html", article=article, next_page=next_page)

# ------------------- REVIEW PANEL -------------------
@app.route('/review_articles', methods=['GET', 'POST'])
def review_articles():
    role = session.get('role')
    if role not in ['admin', 'moderator', 'journalist']:
        flash("Access denied.", "danger")
        return redirect(url_for('personnel_login'))

    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    article_id = request.args.get('article_id')
    article_to_edit = None

    # -------- Journalist Editing Their Article --------
    if role == 'journalist' and article_id:
        article_id = int(article_id)
        cursor.execute(
            "SELECT * FROM articles WHERE id=%s AND author_id=%s",
            (article_id, session['user_id'])
        )
        article_to_edit = cursor.fetchone()

        if not article_to_edit:
            flash("Article not found or access denied.", "danger")
            cursor.close()
            connection.close()
            return redirect(url_for('journalist_dashboard'))

        # Handle Resubmit
        if request.method == 'POST':
            title = (request.form.get('title') or '').strip()
            content = (request.form.get('content') or '').strip()
            category_id = request.form.get('category_id')
            district_id = request.form.get('district_id')
            delete_image = request.form.get('delete_image')
            new_image_file = request.files.get('new_image')
            
            if not title or not content:
                 flash("⚠️ Title and content cannot be empty.", "danger")
            else:
                image_url = article_to_edit['image_url']
                if delete_image == 'yes' and image_url:
                    try:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image_url))
                    except Exception as e:
                        print(f"Failed to delete image: {e}")
                if new_image_file and allowed_file(new_image_file.filename):
                    image_url = save_image(new_image_file)

                cursor.execute("""
                    UPDATE articles 
                    SET title=%s, content=%s, image_url=%s, category_id=%s, district_id=%s, status='pending', rejection_reason=NULL
                    WHERE id=%s AND author_id=%s
                """, (title, content, image_url, category_id, district_id, article_id, session['user_id']))
                connection.commit()

                flash(f"✅ Your article '{title}' has been resubmitted for review.", "success")
                return redirect(url_for('journalist_dashboard'))

        # Load categories and districts for edit form
        cursor.execute("SELECT id, name FROM categories")
        categories = cursor.fetchall()
        cursor.execute("SELECT id, name FROM districts")
        districts = cursor.fetchall()
        next_url = request.args.get('next', url_for('journalist_dashboard'))

        cursor.close()
        connection.close()

        return render_template(
            'review_articles.html',
            article_to_edit=article_to_edit,
            categories=categories,
            districts=districts,
            next_url=next_url
        )

    # -------- Admin / Moderator Review Panel --------
    if role in ['admin', 'moderator']:
        # Handle Approve / Reject
        if request.method == 'POST':
            action_article_id = request.form.get('article_id')
            action = request.form.get('action')
            
            if action_article_id and action in ['approved', 'rejected']:
                cursor.execute("SELECT author_id, title FROM articles WHERE id=%s", (action_article_id,))
                article = cursor.fetchone()
                if not article:
                    flash("Article not found.", "danger")
                    return redirect(url_for('review_articles'))
                author_id = article['author_id']
                title = article['title']
                
                if action == 'approved':
                    cursor.execute(
                        "UPDATE articles SET status='approved', rejection_reason=NULL WHERE id=%s",
                        (action_article_id,))
                    cursor.execute("""
                        INSERT INTO notifications (user_id, article_id, notif_type, message, created_at)
                        VALUES (%s, %s, %s, %s, NOW())
                    """, (author_id, action_article_id, 'approved', f"✅ Your article '{title}' has been approved."))

                elif action == 'rejected':
                    rejection_reason = (request.form.get('rejection_reason') or '').strip()
                    if not rejection_reason:
                        rejection_reason = "No reason provided."
                        
                    cursor.execute("""
                        UPDATE articles 
                        SET status='rejected', rejection_reason=%s 
                        WHERE id=%s
                    """, (rejection_reason, action_article_id))
                    
                    cursor.execute("""
                        INSERT INTO notifications (user_id, article_id, notif_type, message, created_at)
                        VALUES (%s, %s, %s, %s, NOW())
                    """, (author_id, action_article_id, 'rejected',
                          f"Your article '{title}' was rejected. Reason: {rejection_reason}"))
                    
                connection.commit()
                flash(f"Article {action} successfully!", "success")
                return redirect(url_for('review_articles'))


        # Fetch pending articles (with content for modal view)
        cursor.execute("""
            SELECT a.id, a.title, a.content, u.username AS author,
                   c.name AS category_name,
                   d1.name AS main_district_name,
                   d2.name AS second_district_name,
                   a.image_url,
                   a.is_local_voice
            FROM articles a
            LEFT JOIN users u ON a.author_id = u.id
            LEFT JOIN categories c ON a.category_id = c.id
            LEFT JOIN districts d1 ON a.district_id = d1.id
            LEFT JOIN districts d2 ON a.second_district_id = d2.id
            WHERE a.status='pending'
            ORDER BY a.submit_time DESC
            """)
        pending_articles = cursor.fetchall()

        # Fetch reviewed articles
        cursor.execute("""
            SELECT a.id, a.title, a.content, u.username AS author,
                   a.status, a.is_local_voice,
                   c.name AS category_name,
                   d1.name AS main_district_name,
                   d2.name AS second_district_name
            FROM articles a
            LEFT JOIN users u ON a.author_id = u.id
            LEFT JOIN categories c ON a.category_id = c.id
            LEFT JOIN districts d1 ON a.district_id = d1.id
            LEFT JOIN districts d2 ON a.second_district_id = d2.id
            WHERE a.status IN ('approved')
            ORDER BY a.submit_time DESC
            """)
        approved_articles = cursor.fetchall()
        
        cursor.execute("""
            SELECT a.id, a.title, u.username AS author,
                   c.name AS category_name,
                   d1.name AS main_district_name,
                   d2.name AS second_district_name,
                   a.is_local_voice
            FROM articles a
            LEFT JOIN users u ON a.author_id = u.id
            LEFT JOIN categories c ON a.category_id = c.id
            LEFT JOIN districts d1 ON a.district_id = d1.id
            LEFT JOIN districts d2 ON a.second_district_id = d2.id
            WHERE a.status='rejected'
            ORDER BY a.submit_time DESC
        """)
        rejected_articles = cursor.fetchall()

        # redirectors 
        next_url = request.args.get('next')
        if not next_url:
            if role == 'admin':
                next_url = url_for('admin_dashboard')
            elif role == 'moderator':
                next_url = url_for('review_articles')
            elif role == 'journalist':
                next_url = url_for('journalist_dashboard')
            else:
                next_url = url_for('index')

        
        cursor.close()
        connection.close()

        return render_template(
            'review_articles.html',
            pending_articles=pending_articles,
            approved_articles=approved_articles,
            rejected_articles=rejected_articles,
            next_url=next_url
        )

    cursor.close()
    connection.close()
    return redirect(url_for('personnel_login'))

#MODERATOR APPROVE/REJECT ACTION 
@app.route('/personnel/moderator/action', methods=['POST'])
def moderator_action():
    if session.get('role') != 'moderator':
        flash("Access denied.", "danger")
        return redirect(url_for('personnel_login'))

    article_id = request.form.get('article_id')
    action = request.form.get('action')  
    next_page = request.form.get('next') or url_for('moderator_dashboard')
    rejection_reason = request.form.get('rejection_reason', '')
    
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            if action in ['approved', 'rejected']:
                sql = "UPDATE articles SET status=%s"
                params = [action]
                if action == 'rejected':
                    sql += ", rejection_reason=%s"
                    params.append(rejection_reason)
                sql += " WHERE id=%s"
                params.append(article_id)

                cursor.execute(sql, tuple(params))
                connection.commit()
                flash(f"Article {action} successfully!", "success")

                cursor.execute("SELECT author_id, title, is_local_voice FROM articles WHERE id=%s", (article_id,))
                article = cursor.fetchone()
                author_id = article['author_id']
                title = article['title']
                is_local_voice = article['is_local_voice']
                
                # Send notification to author if rejected
                if action == 'approved':
                    if is_local_voice:
                        message=f"Your Local Voice '{title}' was approved. "
                    notif_type = 'approved'
                    
                else: 
                    if is_local_voice:
                        message = f"Your Local Voice '{title}' was rejected."
                    else:
                        message = f"Your Article '{title}' was rejected."
                    if rejection_reason:
                        message += f" Reason : {rejection_reason}"
                    notif_type = 'rejected'
                    
                    cursor.execute(
                    "INSERT INTO notifications (user_id, article_id, type, message) VALUES (%s, %s, %s, %s)",
                    (author_id, article_id, notif_type, message)
                    )
                    connection.commit()
                

            elif action == 'delete':
                cursor.execute("DELETE FROM articles WHERE id=%s", (article_id,))
                connection.commit()
                flash("Article deleted successfully.", "success")

    return redirect(next_page)

    
#-------------------- DELETE ARTICLE -------------------
@app.route('/article/delete/<int:article_id>', methods=['POST', 'GET'])
def delete_article(article_id):
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('personnel_login'))

    next_url = request.form.get('next')
    role = session.get('role')
    with get_db_connection() as connection:
        with connection.cursor() as cursor: 
            cursor.execute("DELETE FROM articles WHERE id=%s", (article_id,))
        connection.commit()
        flash("Article deleted successfully.", "success")
    
    if next_url:
        return redirect(next_url or url_for('review_articles'))
    
# ------------------- MODERATOR -------------------

@app.route('/personnel/moderator')
def moderator_dashboard():
    if session.get('role') != 'moderator':
        flash("Access denied.", "danger")
        return redirect(url_for('personnel_login'))

    session.permanent = True
    user_id = session.get('user_id')

    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    active_tab = request.args.get('tab', 'articles')
            
    statuses = ['draft', 'pending', 'approved', 'rejected']
    articles = {}
    for status in statuses:
        cursor.execute(
        """
        SELECT a.id, a.title, a.content, a.image_url, u.username AS author,
               a.status, a.is_local_voice
        FROM articles a
        JOIN users u ON a.author_id = u.id
        WHERE a.status=%s
        ORDER BY a.submit_time DESC
        """,
        (status,)
        )
        articles[status] = cursor.fetchall()

    cursor.execute("SELECT id, name FROM districts ORDER BY name")
    districts = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template(
        'moderator_dashboard.html',
        user=user,
        articles=articles,
        districts=districts,
        active_tab=active_tab
    )


@app.route('/dismiss_notification/<int:notif_id>', methods=['POST'])
def dismiss_notification(notif_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401

    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Delete or mark as dismissed
    cursor.execute("DELETE FROM notifications WHERE id=%s AND user_id=%s", (notif_id, user_id))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'success': True})

# ------------------- STATIC PAGES -------------------
@app.route('/buzznews/about_us')
def about_us():
    return render_template('about-us.html')


@app.route('/buzznews/editorial_values')
def editorial_values():
    return render_template('editorial_values.html')

@app.route('/buzznews/sitemap')
def sitemap():
    if 'user_id' not in session: 
        flash("Please log in to view the sitemap.", "warning")
        return redirect(url_for('user_login'))
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    today = time.strftime('%Y-%m-%d')
    cursor.execute(""" SELECT a.id, a.title, a.is_local_voice, a.submit_time,
                   u.username AS author,
                   c.name AS category_name,
                   d.name AS district_name
                FROM articles a
                JOIN users u ON a.author_id = u.id
                LEFT JOIN categories c ON a.category_id = c.id
                LEFT JOIN districts d ON a.district_id = d.id
                WHERE DATE(a.submit_time) = %s
                AND a.status = 'approved'
                ORDER BY a.submit_time DESC """, (today,))
    
    articles_today = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return render_template('sitemap.html', articles=articles_today, date=today)

# ------------------- LOGOUT -------------------
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash("You have been logged out!", "success")
    return redirect(url_for('user_login'))


@app.route('/personnel/logout', methods=['POST'])
def personnel_logout():
    session.clear()
    flash("You have been logged out!", "success")
    return redirect(url_for('personnel_login'))


# ------------------- NO CACHE -------------------
@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


# ------------------- RUN -------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        run_db_setup()
    app.run(debug=True)

