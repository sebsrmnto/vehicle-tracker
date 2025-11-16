from flask import Flask, render_template, request, redirect, flash, url_for, Response, session
from db_config import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import os
import csv
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from functools import wraps

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
# Use environment variable for secret key, fallback to default for local development
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-change-me-in-production')
# Set permanent session lifetime (30 days for "remember me" functionality)
app.permanent_session_lifetime = timedelta(days=30)

# Configure session cookies
# Secure cookies are required for HTTPS (production), but break on HTTP (local dev)
# We'll set this dynamically based on the request in a before_request handler
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access (always safe)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection (always safe)

# Set secure cookies only when running behind a proxy (Railway uses HTTPS)
# Railway sets PORT environment variable, and we're behind a proxy
if os.getenv('PORT'):  # Railway sets this
    app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS

# Validation functions
def validate_vehicle_data(brand, model, year, plate):
    """Validate vehicle form data"""
    errors = []
    
    # Brand validation
    if not brand or not brand.strip():
        errors.append("Brand is required.")
    elif len(brand.strip()) > 100:
        errors.append("Brand must be 100 characters or less.")
    
    # Model validation
    if not model or not model.strip():
        errors.append("Model is required.")
    elif len(model.strip()) > 100:
        errors.append("Model must be 100 characters or less.")
    
    # Year validation
    try:
        year_int = int(year)
        current_year = datetime.now().year
        if year_int < 1900 or year_int > current_year + 1:
            errors.append(f"Year must be between 1900 and {current_year + 1}.")
    except (ValueError, TypeError):
        errors.append("Year must be a valid number.")
    
    # Plate validation
    if not plate or not plate.strip():
        errors.append("Plate number is required.")
    elif len(plate.strip()) > 50:
        errors.append("Plate number must be 50 characters or less.")
    
    return errors

def validate_maintenance_data(maintenance_type, maintenance_date, cost=None):
    """Validate maintenance form data"""
    errors = []
    
    # Maintenance type validation
    if not maintenance_type or not maintenance_type.strip():
        errors.append("Maintenance type is required.")
    elif len(maintenance_type.strip()) > 100:
        errors.append("Maintenance type must be 100 characters or less.")
    
    # Date validation
    if not maintenance_date:
        errors.append("Maintenance date is required.")
    else:
        try:
            date_obj = datetime.strptime(maintenance_date, '%Y-%m-%d')
            if date_obj.date() > datetime.now().date():
                errors.append("Maintenance date cannot be in the future.")
        except ValueError:
            errors.append("Invalid date format.")
    
    # Cost validation
    if cost and cost.strip():
        try:
            cost_float = float(cost)
            if cost_float < 0:
                errors.append("Cost cannot be negative.")
            elif cost_float > 999999.99:
                errors.append("Cost is too large.")
        except ValueError:
            errors.append("Cost must be a valid number.")
    
    return errors

# Authentication helper functions
def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user_id():
    """Get the current logged-in user's ID"""
    return session.get('user_id')

@app.route('/')
def home():
    """Landing page - accessible to everyone"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get quick stats for landing page (all users' data for public view)
        cursor.execute("SELECT COUNT(*) as total FROM vehicles")
        total_vehicles = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM maintenance_logs")
        total_maintenance = cursor.fetchone()['total']
        
        cursor.execute("SELECT SUM(cost) as total_cost FROM maintenance_logs WHERE cost IS NOT NULL")
        result = cursor.fetchone()
        total_cost = result['total_cost'] if result['total_cost'] else 0
        
        # Check if user is logged in
        is_logged_in = 'user_id' in session
        
        return render_template('home.html', 
                             total_vehicles=total_vehicles,
                             total_maintenance=total_maintenance,
                             total_cost=total_cost,
                             is_logged_in=is_logged_in)
    except Exception as e:
        app.logger.error(f'Error in home: {str(e)}')
        is_logged_in = 'user_id' in session
        return render_template('home.html', 
                             total_vehicles=0,
                             total_maintenance=0,
                             total_cost=0,
                             is_logged_in=is_logged_in)
    finally:
        if conn:
            conn.close()

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with personal stats"""
    user_id = get_current_user_id()
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get user-specific stats
        cursor.execute("SELECT COUNT(*) as total FROM vehicles WHERE user_id = %s", (user_id,))
        total_vehicles = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM maintenance_logs WHERE user_id = %s", (user_id,))
        total_maintenance = cursor.fetchone()['total']
        
        cursor.execute("SELECT SUM(cost) as total_cost FROM maintenance_logs WHERE user_id = %s AND cost IS NOT NULL", (user_id,))
        result = cursor.fetchone()
        total_cost = result['total_cost'] if result['total_cost'] else 0
        
        return render_template('dashboard.html', 
                             total_vehicles=total_vehicles,
                             total_maintenance=total_maintenance,
                             total_cost=total_cost)
    except Exception as e:
        app.logger.error(f'Error in dashboard: {str(e)}')
        return render_template('dashboard.html', 
                             total_vehicles=0,
                             total_maintenance=0,
                             total_cost=0)
    finally:
        if conn:
            conn.close()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()
        
        # Validate input
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('signup.html', email=email)
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('signup.html', email=email)
        
        if '@' not in email or '.' not in email:
            flash('Please enter a valid email address.', 'error')
            return render_template('signup.html', email=email)
        
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                flash('An account with this email already exists.', 'error')
                return render_template('signup.html', email=email)
            
            # Hash password and create user
            password_hash = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                (email, password_hash)
            )
            conn.commit()
            
            # Get the new user's ID
            user_id = cursor.lastrowid
            
            # Log the user in
            session['user_id'] = user_id
            session['email'] = email
            
            flash('Account created successfully! Welcome to AutoTrack.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            error_msg = str(e)
            app.logger.error(f'Error in signup: {error_msg}', exc_info=True)
            
            # Check if it's a database connection error
            if 'connection' in error_msg.lower() or 'mysql' in error_msg.lower() or 'database' in error_msg.lower():
                flash('Database connection error. Please try again in a moment.', 'error')
            else:
                flash('An error occurred while creating your account. Please try again.', 'error')
            return render_template('signup.html', email=email)
        finally:
            if conn:
                conn.close()
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()
        
        # Validate input
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('login.html', email=email)
        
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Find user by email
            cursor.execute("SELECT id, email, password_hash FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if not user or not check_password_hash(user['password_hash'], password):
                flash('Invalid email or password.', 'error')
                return render_template('login.html', email=email)
            
            # Check if "Remember me" is checked
            remember_me = request.form.get('remember_me') == 'on'
            
            # Log the user in
            session['user_id'] = user['id']
            session['email'] = user['email']
            
            # Set permanent session if "Remember me" is checked
            if remember_me:
                session.permanent = True
            else:
                session.permanent = False
            
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            error_msg = str(e)
            app.logger.error(f'Error in login: {error_msg}', exc_info=True)
            
            # Check if it's a database connection error
            if 'connection' in error_msg.lower() or 'mysql' in error_msg.lower() or 'database' in error_msg.lower():
                flash('Database connection error. Please try again in a moment.', 'error')
            else:
                flash('An error occurred while logging in. Please try again.', 'error')
            return render_template('login.html', email=email)
        finally:
            if conn:
                conn.close()
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/vehicles')
@login_required
def index():
    user_id = get_current_user_id()
    conn = None
    try:
        # Get search query if provided
        search_query = request.args.get('search', '').strip()
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Build search query - search in brand, model, or plate_number (filtered by user)
        if search_query:
            # Sanitize search query to prevent SQL injection (though parameterized queries already protect us)
            search_pattern = f'%{search_query}%'
            cursor.execute(
                "SELECT * FROM vehicles WHERE user_id = %s AND (brand LIKE %s OR model LIKE %s OR plate_number LIKE %s) ORDER BY year DESC",
                (user_id, search_pattern, search_pattern, search_pattern)
            )
        else:
            cursor.execute("SELECT * FROM vehicles WHERE user_id = %s ORDER BY year DESC", (user_id,))
        
        vehicles = cursor.fetchall()
        
        # Calculate statistics (user-specific)
        cursor.execute("SELECT COUNT(*) as total FROM vehicles WHERE user_id = %s", (user_id,))
        total = cursor.fetchone()['total']
        
        cursor.execute("SELECT MIN(year) as oldest, MAX(year) as newest FROM vehicles WHERE user_id = %s", (user_id,))
        stats = cursor.fetchone()
        oldest = stats['oldest'] if stats['oldest'] else 'N/A'
        newest = stats['newest'] if stats['newest'] else 'N/A'
        
        return render_template('index.html', vehicles=vehicles, search_query=search_query, 
                             total=total, oldest=oldest, newest=newest)
    except Exception as e:
        app.logger.error(f'Error in index: {str(e)}')
        flash('An error occurred while loading vehicles. Please try again.', 'error')
        return render_template('index.html', vehicles=[], search_query='', 
                             total=0, oldest='N/A', newest='N/A')
    finally:
        if conn:
            conn.close()

@app.route('/add_vehicle', methods=['GET', 'POST'])
@login_required
def add_vehicle():
    user_id = get_current_user_id()
    if request.method == 'POST':
        brand = request.form.get('brand', '').strip()
        model = request.form.get('model', '').strip()
        year = request.form.get('year', '').strip()
        plate = request.form.get('plate', '').strip()

        # Validate input
        errors = validate_vehicle_data(brand, model, year, plate)
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('add_vehicles.html', 
                                 brand=brand, model=model, year=year, plate=plate)

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if plate number already exists for this user
            cursor.execute("SELECT id FROM vehicles WHERE user_id = %s AND plate_number = %s", (user_id, plate))
            if cursor.fetchone():
                flash('A vehicle with this plate number already exists.', 'error')
                return render_template('add_vehicles.html', 
                                     brand=brand, model=model, year=year, plate=plate)
            
            cursor.execute(
                "INSERT INTO vehicles (user_id, brand, model, year, plate_number) VALUES (%s, %s, %s, %s, %s)",
                (user_id, brand, model, int(year), plate)
            )
            conn.commit()
            flash('Vehicle added successfully.', 'success')
            return redirect(url_for('index'))  # Redirects to /vehicles
        except Exception as e:
            if conn:
                conn.rollback()
            app.logger.error(f'Error adding vehicle: {str(e)}')
            flash('An error occurred while adding the vehicle. Please try again.', 'error')
            return render_template('add_vehicles.html', 
                                 brand=brand, model=model, year=year, plate=plate)
        finally:
            if conn:
                conn.close()
    
    return render_template('add_vehicles.html')

@app.route('/vehicle/<int:vehicle_id>')
@login_required
def view_vehicle(vehicle_id):
    user_id = get_current_user_id()
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vehicles WHERE id = %s AND user_id = %s", (vehicle_id, user_id))
        vehicle = cursor.fetchone()
        
        if not vehicle:
            flash('Vehicle not found.', 'error')
            return redirect(url_for('index'))
        
        # Get maintenance logs for this vehicle (user-specific)
        cursor.execute(
            "SELECT * FROM maintenance_logs WHERE vehicle_id = %s AND user_id = %s ORDER BY maintenance_date DESC",
            (vehicle_id, user_id)
        )
        maintenance_logs = cursor.fetchall()
        
        return render_template('view_log.html', vehicle=vehicle, maintenance_logs=maintenance_logs)
    except Exception as e:
        app.logger.error(f'Error viewing vehicle: {str(e)}')
        flash('An error occurred while loading the vehicle. Please try again.', 'error')
        return redirect(url_for('index'))
    finally:
        if conn:
            conn.close()

@app.route('/edit_vehicle/<int:vehicle_id>', methods=['GET', 'POST'])
@login_required
def edit_vehicle(vehicle_id):
    user_id = get_current_user_id()
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if vehicle exists and belongs to user
        cursor.execute("SELECT * FROM vehicles WHERE id = %s AND user_id = %s", (vehicle_id, user_id))
        vehicle = cursor.fetchone()
        
        if not vehicle:
            flash('Vehicle not found.', 'error')
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            brand = request.form.get('brand', '').strip()
            model = request.form.get('model', '').strip()
            year = request.form.get('year', '').strip()
            plate = request.form.get('plate', '').strip()
            
            # Validate input
            errors = validate_vehicle_data(brand, model, year, plate)
            if errors:
                for error in errors:
                    flash(error, 'error')
                return render_template('edit_vehicle.html', vehicle={
                    'id': vehicle_id,
                    'brand': brand,
                    'model': model,
                    'year': year,
                    'plate_number': plate
                })
            
            # Check if plate number already exists for this user (excluding current vehicle)
            cursor.execute("SELECT id FROM vehicles WHERE user_id = %s AND plate_number = %s AND id != %s", (user_id, plate, vehicle_id))
            if cursor.fetchone():
                flash('A vehicle with this plate number already exists.', 'error')
                return render_template('edit_vehicle.html', vehicle={
                    'id': vehicle_id,
                    'brand': brand,
                    'model': model,
                    'year': year,
                    'plate_number': plate
                })
            
            try:
                cursor.execute(
                    "UPDATE vehicles SET brand = %s, model = %s, year = %s, plate_number = %s WHERE id = %s AND user_id = %s",
                    (brand, model, int(year), plate, vehicle_id, user_id)
                )
                conn.commit()
                flash('Vehicle updated successfully.', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                conn.rollback()
                app.logger.error(f'Error updating vehicle: {str(e)}')
                flash('An error occurred while updating the vehicle. Please try again.', 'error')
                return render_template('edit_vehicle.html', vehicle=vehicle)
        
        return render_template('edit_vehicle.html', vehicle=vehicle)
    except Exception as e:
        app.logger.error(f'Error in edit_vehicle: {str(e)}')
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('index'))
    finally:
        if conn:
            conn.close()

@app.route('/delete_vehicle/<int:vehicle_id>', methods=['POST'])
@login_required
def delete_vehicle(vehicle_id):
    user_id = get_current_user_id()
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if vehicle exists and belongs to user
        cursor.execute("SELECT id FROM vehicles WHERE id = %s AND user_id = %s", (vehicle_id, user_id))
        if not cursor.fetchone():
            flash('Vehicle not found.', 'error')
            return redirect(url_for('index'))
        
        cursor.execute("DELETE FROM vehicles WHERE id = %s AND user_id = %s", (vehicle_id, user_id))
        conn.commit()
        flash('Vehicle deleted successfully.', 'success')
    except Exception as e:
        if conn:
            conn.rollback()
        app.logger.error(f'Error deleting vehicle: {str(e)}')
        flash('An error occurred while deleting the vehicle. Please try again.', 'error')
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('index'))

@app.route('/add_maintenance/<int:vehicle_id>', methods=['GET', 'POST'])
@login_required
def add_maintenance(vehicle_id):
    user_id = get_current_user_id()
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verify vehicle exists and belongs to user
        cursor.execute("SELECT * FROM vehicles WHERE id = %s AND user_id = %s", (vehicle_id, user_id))
        vehicle = cursor.fetchone()
        
        if not vehicle:
            flash('Vehicle not found.', 'error')
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            maintenance_type = request.form.get('maintenance_type', '').strip()
            description = request.form.get('description', '').strip()
            cost = request.form.get('cost', '').strip()
            maintenance_date = request.form.get('maintenance_date', '').strip()
            
            # Validate input
            errors = validate_maintenance_data(maintenance_type, maintenance_date, cost)
            if errors:
                for error in errors:
                    flash(error, 'error')
                return render_template('add_maintenance.html', vehicle=vehicle)
            
            # Convert cost to None if empty
            cost_value = float(cost) if cost else None
            
            # Validate description length
            if description and len(description) > 65535:  # TEXT field max length
                flash('Description is too long.', 'error')
                return render_template('add_maintenance.html', vehicle=vehicle)
            
            try:
                cursor.execute(
                    """INSERT INTO maintenance_logs 
                       (vehicle_id, user_id, maintenance_type, description, cost, maintenance_date) 
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (vehicle_id, user_id, maintenance_type, description or None, cost_value, maintenance_date)
                )
                conn.commit()
                flash('Maintenance log added successfully.', 'success')
                return redirect(url_for('view_vehicle', vehicle_id=vehicle_id))
            except Exception as e:
                conn.rollback()
                app.logger.error(f'Error adding maintenance: {str(e)}')
                flash('An error occurred while adding the maintenance log. Please try again.', 'error')
                return render_template('add_maintenance.html', vehicle=vehicle)
        
        return render_template('add_maintenance.html', vehicle=vehicle)
    except Exception as e:
        app.logger.error(f'Error in add_maintenance: {str(e)}')
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('index'))
    finally:
        if conn:
            conn.close()

@app.route('/delete_maintenance/<int:maintenance_id>', methods=['POST'])
@login_required
def delete_maintenance(maintenance_id):
    user_id = get_current_user_id()
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get vehicle_id before deleting (to redirect back) - verify it belongs to user
        cursor.execute("SELECT vehicle_id FROM maintenance_logs WHERE id = %s AND user_id = %s", (maintenance_id, user_id))
        result = cursor.fetchone()
        
        if not result:
            flash('Maintenance log not found.', 'error')
            return redirect(url_for('index'))
        
        vehicle_id = result['vehicle_id']
        
        cursor.execute("DELETE FROM maintenance_logs WHERE id = %s AND user_id = %s", (maintenance_id, user_id))
        conn.commit()
        flash('Maintenance log deleted successfully.', 'success')
        return redirect(url_for('view_vehicle', vehicle_id=vehicle_id))
    except Exception as e:
        if conn:
            conn.rollback()
        app.logger.error(f'Error deleting maintenance: {str(e)}')
        flash('An error occurred while deleting the maintenance log. Please try again.', 'error')
        return redirect(url_for('index'))
    finally:
        if conn:
            conn.close()

# Serve web manifest
@app.route('/site.webmanifest')
def webmanifest():
    from flask import jsonify
    manifest = {
        "name": "AutoTrack - Vehicle Maintenance Tracker",
        "short_name": "AutoTrack",
        "icons": [
            {
                "src": url_for('static', filename='web-app-manifest-192x192.png'),
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": url_for('static', filename='web-app-manifest-512x512.png'),
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ],
        "theme_color": "#1d2939",
        "background_color": "#ffffff",
        "display": "standalone"
    }
    return jsonify(manifest), 200, {'Content-Type': 'application/manifest+json'}

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    flash('Page not found.', 'error')
    return redirect(url_for('index')), 404

@app.errorhandler(500)
def internal_error(error):
    conn = None
    try:
        if conn:
            conn.rollback()
    except:
        pass
    flash('An internal error occurred. Please try again later.', 'error')
    return redirect(url_for('index')), 500

# CSV Export route
@app.route('/export/csv')
@login_required
def export_csv():
    user_id = get_current_user_id()
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vehicles WHERE user_id = %s ORDER BY year DESC", (user_id,))
        vehicles = cursor.fetchall()
        
        # Create CSV in memory
        output = []
        output.append(['ID', 'Brand', 'Model', 'Year', 'Plate Number', 'Created At'])
        
        for vehicle in vehicles:
            output.append([
                vehicle['id'],
                vehicle['brand'],
                vehicle['model'],
                vehicle['year'],
                vehicle['plate_number'],
                vehicle.get('created_at', '').strftime('%Y-%m-%d %H:%M:%S') if vehicle.get('created_at') else ''
            ])
        
        # Generate CSV with proper escaping
        def generate():
            import io
            output_buffer = io.StringIO()
            writer = csv.writer(output_buffer)
            for row in output:
                writer.writerow(row)
            return output_buffer.getvalue()
        
        response = Response(
            generate(),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=vehicles_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'}
        )
        return response
    except Exception as e:
        app.logger.error(f'Error exporting CSV: {str(e)}')
        flash('An error occurred while exporting data. Please try again.', 'error')
        return redirect(url_for('index'))
    finally:
        if conn:
            conn.close()

@app.route('/test-db')
def test_db():
    """
    Diagnostic endpoint to test database connection and configuration.
    Visit this URL to check if database is properly configured.
    """
    results = {
        'database_connection': '❌ Failed',
        'tables_exist': [],
        'environment_variables': {},
        'errors': []
    }
    
    # Check environment variables (mask sensitive data)
    env_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'DB_PORT', 'SECRET_KEY']
    for var in env_vars:
        value = os.getenv(var)
        if value:
            if 'PASSWORD' in var or 'SECRET' in var:
                results['environment_variables'][var] = '***SET***' if value else '❌ NOT SET'
            else:
                results['environment_variables'][var] = value
        else:
            results['environment_variables'][var] = '❌ NOT SET'
    
    # Test database connection
    conn = None
    try:
        conn = get_db_connection()
        results['database_connection'] = '✅ Connected'
        
        # Check which tables exist
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables] if tables else []
        
        # Check for required tables
        required_tables = ['users', 'vehicles', 'maintenance_logs']
        for table in required_tables:
            if table in table_names:
                results['tables_exist'].append(f'✅ {table}')
            else:
                results['tables_exist'].append(f'❌ {table} (MISSING!)')
                results['errors'].append(f'Table "{table}" does not exist. Run setup_database.sql')
        
        # Check users table structure
        if 'users' in table_names:
            cursor.execute("DESCRIBE users")
            columns = cursor.fetchall()
            column_names = [col[0] for col in columns]
            if 'password_hash' not in column_names:
                results['errors'].append('users table missing "password_hash" column')
            if 'email' not in column_names:
                results['errors'].append('users table missing "email" column')
        
        cursor.close()
        
    except Exception as e:
        error_msg = str(e)
        results['database_connection'] = f'❌ Failed: {error_msg}'
        results['errors'].append(f'Database connection error: {error_msg}')
        app.logger.error(f'Database test failed: {error_msg}', exc_info=True)
    finally:
        if conn:
            conn.close()
    
    # Generate HTML response
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Database Diagnostic Test</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #1a1a1a; color: #fff; }}
            h1 {{ color: #4CAF50; }}
            h2 {{ color: #2196F3; margin-top: 30px; }}
            .success {{ color: #4CAF50; }}
            .error {{ color: #f44336; }}
            .info {{ background: #2a2a2a; padding: 15px; border-radius: 5px; margin: 10px 0; }}
            ul {{ list-style: none; padding: 0; }}
            li {{ padding: 5px 0; }}
            a {{ color: #2196F3; }}
        </style>
    </head>
    <body>
        <h1>🔍 Database Diagnostic Test</h1>
        
        <div class="info">
            <h2>Database Connection</h2>
            <p><strong>{results['database_connection']}</strong></p>
        </div>
        
        <div class="info">
            <h2>Environment Variables</h2>
            <ul>
    """
    for var, value in results['environment_variables'].items():
        html += f"<li><strong>{var}:</strong> {value}</li>"
    
    html += """
            </ul>
        </div>
        
        <div class="info">
            <h2>Database Tables</h2>
            <ul>
    """
    for table_status in results['tables_exist']:
        html += f"<li>{table_status}</li>"
    
    html += """
            </ul>
        </div>
    """
    
    if results['errors']:
        html += """
        <div class="info" style="background: #3a1a1a; border-left: 4px solid #f44336;">
            <h2 class="error">⚠️ Issues Found</h2>
            <ul>
        """
        for error in results['errors']:
            html += f"<li class='error'>{error}</li>"
        html += """
            </ul>
        </div>
        """
    
    html += """
        <div class="info">
            <p><a href="/">← Back to Home</a></p>
            <p><small>This diagnostic page helps troubleshoot database connection issues.</small></p>
        </div>
    </body>
    </html>
    """
    
    return html

if __name__ == '__main__':
    # Use environment variable for debug mode, default to False for production
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
