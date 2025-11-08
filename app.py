from flask import Flask, render_template, request, redirect, flash, url_for
from db_config import get_db_connection
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Use environment variable for secret key, fallback to default for local development
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-change-me-in-production')

@app.route('/')
def index():
    # Get search query if provided
    search_query = request.args.get('search', '').strip()
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Build search query - search in brand, model, or plate_number
    if search_query:
        cursor.execute(
            "SELECT * FROM vehicles WHERE brand LIKE %s OR model LIKE %s OR plate_number LIKE %s ORDER BY year DESC",
            (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')
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
    
    conn.close()
    
    return render_template('index.html', vehicles=vehicles, search_query=search_query, 
                         total=total, oldest=oldest, newest=newest)

@app.route('/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        year = request.form['year']
        plate = request.form['plate']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO vehicles (brand, model, year, plate_number) VALUES (%s, %s, %s, %s)",
                (brand, model, year, plate)
            )
            conn.commit()
            flash('Vehicle added successfully.', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Failed to add vehicle: {e}', 'error')
        finally:
            conn.close()
        return redirect(url_for('index'))
    
    return render_template('add_vehicles.html')

@app.route('/vehicle/<int:vehicle_id>')
def view_vehicle(vehicle_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
    vehicle = cursor.fetchone()
    
    if not vehicle:
        conn.close()
        flash('Vehicle not found.', 'error')
        return redirect(url_for('index'))
    
    # Get maintenance logs for this vehicle
    cursor.execute(
        "SELECT * FROM maintenance_logs WHERE vehicle_id = %s ORDER BY maintenance_date DESC",
        (vehicle_id,)
    )
    maintenance_logs = cursor.fetchall()
    
    conn.close()
    return render_template('view_log.html', vehicle=vehicle, maintenance_logs=maintenance_logs)

@app.route('/edit_vehicle/<int:vehicle_id>', methods=['GET', 'POST'])
def edit_vehicle(vehicle_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        year = request.form['year']
        plate = request.form['plate']
        
        try:
            cursor.execute(
                "UPDATE vehicles SET brand = %s, model = %s, year = %s, plate_number = %s WHERE id = %s",
                (brand, model, year, plate, vehicle_id)
            )
            conn.commit()
            flash('Vehicle updated successfully.', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Failed to update vehicle: {e}', 'error')
        finally:
            conn.close()
        return redirect(url_for('index'))
    
    cursor.execute("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
    vehicle = cursor.fetchone()
    conn.close()
    
    if not vehicle:
        flash('Vehicle not found.', 'error')
        return redirect(url_for('index'))
    
    return render_template('edit_vehicle.html', vehicle=vehicle)

@app.route('/delete_vehicle/<int:vehicle_id>', methods=['POST'])
def delete_vehicle(vehicle_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM vehicles WHERE id = %s", (vehicle_id,))
        conn.commit()
        flash('Vehicle deleted successfully.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Failed to delete vehicle: {e}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('index'))

@app.route('/add_maintenance/<int:vehicle_id>', methods=['GET', 'POST'])
def add_maintenance(vehicle_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Verify vehicle exists
    cursor.execute("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
    vehicle = cursor.fetchone()
    
    if not vehicle:
        conn.close()
        flash('Vehicle not found.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        maintenance_type = request.form['maintenance_type']
        description = request.form.get('description', '')
        cost = request.form.get('cost', '')
        maintenance_date = request.form['maintenance_date']
        
        # Convert cost to None if empty
        cost_value = float(cost) if cost else None
        
        try:
            cursor.execute(
                """INSERT INTO maintenance_logs 
                   (vehicle_id, maintenance_type, description, cost, maintenance_date) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (vehicle_id, maintenance_type, description, cost_value, maintenance_date)
            )
            conn.commit()
            flash('Maintenance log added successfully.', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Failed to add maintenance log: {e}', 'error')
        finally:
            conn.close()
        return redirect(url_for('view_vehicle', vehicle_id=vehicle_id))
    
    conn.close()
    return render_template('add_maintenance.html', vehicle=vehicle)

@app.route('/delete_maintenance/<int:maintenance_id>', methods=['POST'])
def delete_maintenance(maintenance_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get vehicle_id before deleting (to redirect back)
    cursor.execute("SELECT vehicle_id FROM maintenance_logs WHERE id = %s", (maintenance_id,))
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        flash('Maintenance log not found.', 'error')
        return redirect(url_for('index'))
    
    vehicle_id = result['vehicle_id']
    
    try:
        cursor.execute("DELETE FROM maintenance_logs WHERE id = %s", (maintenance_id,))
        conn.commit()
        flash('Maintenance log deleted successfully.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Failed to delete maintenance log: {e}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('view_vehicle', vehicle_id=vehicle_id))

if __name__ == '__main__':
    # Use environment variable for debug mode, default to False for production
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
