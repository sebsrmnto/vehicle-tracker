from flask import Flask, render_template, request, redirect, flash, url_for, Response
from db_config import get_db_connection
import os
import csv
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Use environment variable for secret key, fallback to default for local development
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-change-me-in-production')

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

@app.route('/')
def home():
    """Landing page"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get quick stats for landing page
        cursor.execute("SELECT COUNT(*) as total FROM vehicles")
        total_vehicles = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM maintenance_logs")
        total_maintenance = cursor.fetchone()['total']
        
        cursor.execute("SELECT SUM(cost) as total_cost FROM maintenance_logs WHERE cost IS NOT NULL")
        result = cursor.fetchone()
        total_cost = result['total_cost'] if result['total_cost'] else 0
        
        return render_template('home.html', 
                             total_vehicles=total_vehicles,
                             total_maintenance=total_maintenance,
                             total_cost=total_cost)
    except Exception as e:
        app.logger.error(f'Error in home: {str(e)}')
        return render_template('home.html', 
                             total_vehicles=0,
                             total_maintenance=0,
                             total_cost=0)
    finally:
        if conn:
            conn.close()

@app.route('/vehicles')
def index():
    conn = None
    try:
        # Get search query if provided
        search_query = request.args.get('search', '').strip()
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Build search query - search in brand, model, or plate_number
        if search_query:
            # Sanitize search query to prevent SQL injection (though parameterized queries already protect us)
            search_pattern = f'%{search_query}%'
            cursor.execute(
                "SELECT * FROM vehicles WHERE brand LIKE %s OR model LIKE %s OR plate_number LIKE %s ORDER BY year DESC",
                (search_pattern, search_pattern, search_pattern)
            )
        else:
            cursor.execute("SELECT * FROM vehicles ORDER BY year DESC")
        
        vehicles = cursor.fetchall()
        
        # Calculate statistics
        cursor.execute("SELECT COUNT(*) as total FROM vehicles")
        total = cursor.fetchone()['total']
        
        cursor.execute("SELECT MIN(year) as oldest, MAX(year) as newest FROM vehicles")
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
def add_vehicle():
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
            
            # Check if plate number already exists
            cursor.execute("SELECT id FROM vehicles WHERE plate_number = %s", (plate,))
            if cursor.fetchone():
                flash('A vehicle with this plate number already exists.', 'error')
                return render_template('add_vehicles.html', 
                                     brand=brand, model=model, year=year, plate=plate)
            
            cursor.execute(
                "INSERT INTO vehicles (brand, model, year, plate_number) VALUES (%s, %s, %s, %s)",
                (brand, model, int(year), plate)
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
def view_vehicle(vehicle_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
        vehicle = cursor.fetchone()
        
        if not vehicle:
            flash('Vehicle not found.', 'error')
            return redirect(url_for('index'))
        
        # Get maintenance logs for this vehicle
        cursor.execute(
            "SELECT * FROM maintenance_logs WHERE vehicle_id = %s ORDER BY maintenance_date DESC",
            (vehicle_id,)
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
def edit_vehicle(vehicle_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if vehicle exists
        cursor.execute("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
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
            
            # Check if plate number already exists (excluding current vehicle)
            cursor.execute("SELECT id FROM vehicles WHERE plate_number = %s AND id != %s", (plate, vehicle_id))
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
                    "UPDATE vehicles SET brand = %s, model = %s, year = %s, plate_number = %s WHERE id = %s",
                    (brand, model, int(year), plate, vehicle_id)
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
def delete_vehicle(vehicle_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if vehicle exists
        cursor.execute("SELECT id FROM vehicles WHERE id = %s", (vehicle_id,))
        if not cursor.fetchone():
            flash('Vehicle not found.', 'error')
            return redirect(url_for('index'))
        
        cursor.execute("DELETE FROM vehicles WHERE id = %s", (vehicle_id,))
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
def add_maintenance(vehicle_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verify vehicle exists
        cursor.execute("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
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
                       (vehicle_id, maintenance_type, description, cost, maintenance_date) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (vehicle_id, maintenance_type, description or None, cost_value, maintenance_date)
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
def delete_maintenance(maintenance_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get vehicle_id before deleting (to redirect back)
        cursor.execute("SELECT vehicle_id FROM maintenance_logs WHERE id = %s", (maintenance_id,))
        result = cursor.fetchone()
        
        if not result:
            flash('Maintenance log not found.', 'error')
            return redirect(url_for('index'))
        
        vehicle_id = result['vehicle_id']
        
        cursor.execute("DELETE FROM maintenance_logs WHERE id = %s", (maintenance_id,))
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
def export_csv():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vehicles ORDER BY year DESC")
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

if __name__ == '__main__':
    # Use environment variable for debug mode, default to False for production
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
