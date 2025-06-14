from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL connection config - change accordingly
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Karasuno10',
        database='skydiv'
    )

@app.route('/')
def index():
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()

        cursor.execute("SELECT * FROM instructors")
        instructors = cursor.fetchall()

        cursor.execute("SELECT * FROM equipment")
        equipments = cursor.fetchall()

        cursor.execute("SELECT * FROM bookings")
        bookings = cursor.fetchall()

        cursor.execute("SELECT * FROM payments")
        payments = cursor.fetchall()

        cursor.execute("SELECT * FROM jump_logs")
        jump_logs = cursor.fetchall()

    except Error as e:
        return f"Database error: {e}", 500
    finally:
        cursor.close()
        cnx.close()

    return render_template('index.html', clients=clients, instructors=instructors,
                           equipments=equipments, bookings=bookings,
                           payments=payments, jump_logs=jump_logs)

@app.route('/add_client', methods=['POST'])
def add_client():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO clients (name, email, phone) VALUES (%s, %s, %s)",
                       (name, email, phone))
        cnx.commit()
    except Error as e:
        cnx.rollback()
        return f"Error adding client: {e}", 500
    finally:
        cursor.close()
        cnx.close()

    return redirect(url_for('index'))

@app.route('/add_instructor', methods=['POST'])
def add_instructor():
    name = request.form['name']
    experience = request.form['experience']

    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO instructors (name, experience) VALUES (%s, %s)",
                       (name, experience))
        cnx.commit()
    except Error as e:
        cnx.rollback()
        return f"Error adding instructor: {e}", 500
    finally:
        cursor.close()
        cnx.close()

    return redirect(url_for('index'))

@app.route('/add_equipment', methods=['POST'])
def add_equipment():
    type_ = request.form['type']
    status = request.form['status']

    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO equipment(type, status) VALUES (%s, %s)", (type_, status))
        cnx.commit()
    except Error as e:
        cnx.rollback()
        return f"Error adding equipment: {e}", 500
    finally:
        cursor.close()
        cnx.close()

    return redirect(url_for('index'))


@app.route('/add_booking', methods=['POST'])
def add_booking():
    client_id = request.form['client_id']
    instructor_id = request.form['instructor_id']
    equipment_id = request.form['equipment_id']
    date = request.form['date']

    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute(
            "INSERT INTO bookings (client_id, instructor_id, equipment_id, date) VALUES (%s, %s, %s, %s)",
            (client_id, instructor_id, equipment_id, date))
        cnx.commit()
    except Error as e:
        cnx.rollback()
        return f"Error adding booking: {e}", 500
    finally:
        cursor.close()
        cnx.close()

    return redirect(url_for('index'))

@app.route('/add_payment', methods=['POST'])
def add_payment():
    booking_id = request.form['booking_id']
    amount = request.form['amount']
    date = request.form['payment_date']

    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute(
            "INSERT INTO payments (booking_id, amount, payment_date) VALUES (%s, %s, %s)",
            (booking_id, amount, date))
        cnx.commit()
    except Error as e:
        cnx.rollback()
        return f"Error adding payment: {e}", 500
    finally:
        cursor.close()
        cnx.close()

    return redirect(url_for('index'))

@app.route('/add_jump_log', methods=['POST'])
def add_jump_log():
    client_id = request.form['client_id']
    instructor_id = request.form['instructor_id']
    equipment_id = request.form['equipment_id']
    jump_date = request.form['jump_date']

    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute(
            "INSERT INTO jump_logs (client_id, instructor_id, equipment_id, jump_date) VALUES (%s, %s, %s, %s)",
            (client_id, instructor_id, equipment_id, jump_date))
        cnx.commit()
    except Error as e:
        cnx.rollback()
        return f"Error adding jump log: {e}", 500
    finally:
        cursor.close()
        cnx.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5050)
