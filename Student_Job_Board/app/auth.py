from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import mysql
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Connect to MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Check if the email exists in the employers_contact table
        cursor.execute("SELECT * FROM employers_contact WHERE email_1 = %s", (email,))
        employer_contact = cursor.fetchone()
        
        cursor.execute("SELECT * FROM student_contact WHERE email_1 = %s", (email,))
        student_contact = cursor.fetchone()
    
        cursor.close()
        
        if employer_contact:
            employer_id = employer_contact['employer_id']  # Get employer_id from employers_contact
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM employer WHERE employer_id = %s", (employer_id,))
            employer = cursor.fetchone()
            cursor.close()
            
            if employer and check_password_hash(employer['password_hash'], password):
                # Log in the employer
                session['loggedin'] = True
                session['user_type'] = 'employer'
                session['employer_id'] = employer_id
                session['email'] = email
                flash("Logged in successfully", category='success')
                return redirect(url_for('employer_profile'))
            else:
                flash("Incorrect email or password", category='error')
            
        elif student_contact:
            student_id = student_contact['student_id']  # Get employer_id from employers_contact
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM student WHERE student_id = %s", (student_id,))
            student = cursor.fetchone()
            cursor.close()
            
            if student and check_password_hash(student['password_hash'], password):
                # Log in the employer
                session['loggedin'] = True
                session['user_type'] = 'student'
                session['student_id'] = student_id
                session['email'] = email
                flash("Logged in successfully", category='success')
                return redirect(url_for('student_profile'))
            else:
                flash("Incorrect email or password", category='error')
        else:
            flash("Incorrect email or werwerpassword", category='error')

        cursor.close()

    return render_template('login.html')

@auth.route('/guest-login', methods=['GET', 'POST'])
def guest_login():
    session['loggedin'] = True
    session['user_type'] = 'guest'
    return redirect(url_for('student_dashboard'))


@auth.route('/student-sign-up', methods=['GET', 'POST'])
def student_sign_up():
    if request.method == 'POST':
        forename = request.form.get('forename')
        surname = request.form.get('surname')
        email_1 = request.form.get('email_1')
        email_2 = request.form.get('email_2')
        phone1 = request.form.get('phone1')
        phone2 = request.form.get('phone2')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        postal_code1 = request.form.get('postal_code1')
        postal_code2 = request.form.get('postal_code2')
        nationality = request.form.get('nationality')
        day = request.form.get('day')
        month = request.form.get('month')
        year = request.form.get('year')
        gender = request.form.get('gender')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        
        date_of_birth = f"{year}-{month}-{day}"
        
        print(forename, surname, email_1, email_2, phone1, phone2, address1, address2, postal_code1, postal_code2, nationality, date_of_birth, password1, password2)
        # Form validation
        if not (forename and surname and email_1 and phone1 and address1 and postal_code1 and nationality and day and month and year and password1 and password2):
            flash('Please fill in all required fields', category='error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_1):
            flash('Invalid email address', category='error')
        elif len(forename) < 2 or len(surname) < 2:
            flash('Forename and surname must be at least 2 characters', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif not re.match(r'^\+?\d{10,15}$', phone1) or (phone2 and not re.match(r'^\+?\d{10,15}$', phone2)):
            flash('Invalid phone number format', category='error')
        else:
            # Hash the password before storing
            hashed_password = generate_password_hash(password1)

            # Insert student data into the database
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO student (forename, surname, password_hash, date_of_birth, gender, nationality) VALUES (%s, %s, %s, %s, %s, %s)", (forename, surname, hashed_password, date_of_birth, gender, nationality))
            student_id = cur.lastrowid  # Get the ID of the inserted student

            # Insert address data into the database
            cur.execute("INSERT INTO student_address (student_id, address_line_1, address_line_2, postal_code_1, postal_code_2) VALUES (%s, %s, %s, %s, %s)", (student_id, address1, address2, postal_code1, postal_code2))

            # Insert contact data into the database
            cur.execute("INSERT INTO student_contact (student_id, phone_number_1, phone_number_2, email_1, email_2) VALUES (%s, %s, %s, %s, %s)", (student_id, phone1, phone2, email_1, email_2))

            mysql.connection.commit()
            cur.close()

            flash('Student account created successfully', category='success')
            return redirect(url_for('auth.login'))  # Redirect to login page after successful sign-up

    return render_template('student_sign_up.html')



@auth.route('/edit-student-profile', methods=['GET', 'POST'])
def edit_student_profile():
    if 'loggedin' in session and 'student_id' in session:
        student_id = session['student_id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student JOIN student_address ON student.student_id = student_address.student_id JOIN student_contact ON student.student_id = student_contact.student_id WHERE student.student_id = %s", (student_id,))
        user = cur.fetchone()  # Fetch the user information
        cur.close()

        if request.method == 'POST':
            forename = request.form.get('forename').capitalize()
            surname = request.form.get('surname').capitalize()
            email_1 = request.form.get('email_1')
            email_2 = request.form.get('email_2')
            phone1 = request.form.get('phone1')
            phone2 = request.form.get('phone2')
            address1 = request.form.get('address1')
            postal_code1 = request.form.get('postal_code1')
            address2 = request.form.get('address2')
            postal_code2 = request.form.get('postal_code2')
            gender = request.form.get('gender')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')

            # Form validation
            # Form validation
            if len(email_1) < 4:
                flash("Email must be greater than 4 characters", category='error')
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email_1):
                flash("Invalid email address", category='error')
            elif len(forename) < 2:
                flash("Forename must be greater than 2 characters", category='error')
            elif len(surname) < 2:
                flash("Surname must be greater than 2 characters", category='error')
            elif password1 and len(password1) < 7:
                flash("Password must be at least 7 characters", category='error')
            elif password1 != password2:
                flash("Passwords don't match", category='error')
            elif not gender:
                flash("Please select a gender", category='error')
            else:
                # Update user information in the database
                cur = mysql.connection.cursor()
                if password1:
                    hashed_password = generate_password_hash(password1)
                    cur.execute("UPDATE student SET forename = %s, surname = %s, password_hash = %s, gender = %s WHERE student_id = %s", (forename, surname, hashed_password, gender, student_id))
                    cur.execute("UPDATE student_address SET address_line_1 = %s, address_line_2 = %s, postal_code_1 = %s, postal_code_2 = %s WHERE student_id = %s", (address1, address2, postal_code1, postal_code2, student_id))
                    cur.execute("UPDATE student_contact SET phone_number_1 = %s, phone_number_2 = %s, email_1 = %s, email_2 = %s WHERE student_id = %s", (phone1, phone2, email_1, email_2, student_id))
                else:
                    cur.execute("UPDATE student SET forename = %s, surname = %s, gender = %s WHERE student_id = %s", (forename, surname, gender, student_id))
                    cur.execute("UPDATE student_address SET address_line_1 = %s, address_line_2 = %s, postal_code_1 = %s, postal_code_2 = %s WHERE student_id = %s", (address1, address2, postal_code1, postal_code2, student_id))
                    cur.execute("UPDATE student_contact SET phone_number_1 = %s, phone_number_2 = %s, email_1 = %s, email_2 = %s WHERE student_id = %s", (phone1, phone2, email_1, email_2, student_id))

                mysql.connection.commit()
                cur.close()

                flash("Profile updated successfully", category='success')
                return redirect(url_for('student_profile'))

        # Pre-fill the form fields with existing information
        return render_template('student_edit_profile.html', user=user)
    else:
        flash("Please log in as a student to access this page", category='error')
        return redirect(url_for('auth.login'))

            
@auth.route('/employer-sign-up', methods=['GET', 'POST'])
def employer_sign_up():
    if request.method == 'POST':
        # Fetch form data
        email1 = request.form.get('email1')
        email2 = request.form.get('email2')
        company = request.form.get('company')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        phone1 = request.form.get('phone1')
        phone2 = request.form.get('phone2')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        postal_code1 = request.form.get('postal_code1')
        postal_code2 = request.form.get('postal_code2')

        # Form validation
        if not (email1 and company and password1 and password2 and phone1 and address1 and postal_code1):
            flash('Please fill in all required fields', category='error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email1):
            flash('Invalid email address', category='error')
        elif len(company) < 2:
            flash('Company name must be at least 2 characters', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif not re.match(r'^\+?\d{10,15}$', phone1) or (phone2 and not re.match(r'^\+?\d{10,15}$', phone2)):
            flash('Invalid phone number format', category='error')
        else:
            # Hash the password before storing
            hashed_password = generate_password_hash(password1)

            # Insert employer data into the database
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO employer (company, password_hash) VALUES (%s, %s)", (company, hashed_password))
            employer_id = cur.lastrowid  # Get the ID of the inserted employer

            # Insert address data into the database
            cur.execute("INSERT INTO employers_address (employer_id, address_line_1, address_line_2, postal_code_1, postal_code_2) VALUES (%s, %s, %s, %s, %s)", (employer_id, address1, address2, postal_code1, postal_code2))

            # Insert contact data into the database
            cur.execute("INSERT INTO employers_contact (employer_id, phone_number_1, phone_number_2, email_1, email_2) VALUES (%s, %s, %s, %s, %s)", (employer_id, phone1, phone2, email1, email2))

            mysql.connection.commit()
            cur.close()

            flash('Employer account created successfully', category='success')
            return redirect(url_for('auth.login'))  # Redirect to login page after successful sign-up

    return render_template('employer_sign_up.html')

@auth.route('/edit-employer-profile', methods=['GET', 'POST'])
def employer_edit_profile():
    if 'loggedin' in session and 'employer_id' in session:
        employer_id = session['employer_id']
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT employer.*, employers_address.*, employers_contact.*
            FROM employer
            LEFT JOIN employers_address ON employer.employer_id = employers_address.employer_id
            LEFT JOIN employers_contact ON employer.employer_id = employers_contact.employer_id
            WHERE employer.employer_id = %s
        """, (employer_id,))
        user_data = cur.fetchone()  # Fetch the user information
        cur.close()

        if request.method == 'POST':
            # Fetch form data
            email1 = request.form.get('email1')
            email2 = request.form.get('email2')
            company = request.form.get('company')
            phone1 = request.form.get('phone1')
            phone2 = request.form.get('phone2')
            address1 = request.form.get('address1')
            address2 = request.form.get('address2')
            postal_code1 = request.form.get('postal_code1')
            postal_code2 = request.form.get('postal_code2')
            description = request.form.get('description')
            website = request.form.get('website')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')

            # Form validation
            if not (email1 and company and phone1 and address1 and postal_code1):
                flash('Please fill in all required fields', category='error')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email1):
                flash('Invalid email address', category='error')
            elif len(company) < 2:
                flash('Company name must be at least 2 characters', category='error')
            elif not re.match(r'^\+?\d{10,15}$', phone1) or (phone2 and not re.match(r'^\+?\d{10,15}$', phone2)):
                flash('Invalid phone number format', category='error')
            elif password1 != password2:
                flash('Passwords do not match', category='error')
            elif len(password1) < 7:
                flash('Password must be at least 7 characters', category='error')
            else:
                # Hash the password before storing
                hashed_password = generate_password_hash(password1)

                # Update employer data in the database
                cur = mysql.connection.cursor()
                cur.execute("""
                    UPDATE employer
                    SET company = %s, description = %s, website = %s, password_hash = %s
                    WHERE employer_id = %s
                """, (company, description, website, hashed_password, employer_id))

                # Update address data in the database
                cur.execute("""
                    UPDATE employers_address
                    SET address_line_1 = %s, address_line_2 = %s, postal_code_1 = %s, postal_code_2 = %s
                    WHERE employer_id = %s
                """, (address1, address2, postal_code1, postal_code2, employer_id))

                # Update contact data in the database
                cur.execute("""
                    UPDATE employers_contact
                    SET phone_number_1 = %s, phone_number_2 = %s, email_1 = %s, email_2 = %s
                    WHERE employer_id = %s
                """, (phone1, phone2, email1, email2, employer_id))

                mysql.connection.commit()
                cur.close()

                flash('Profile updated successfully', category='success')
                return redirect(url_for('employer_profile'))

    return render_template('employer_edit_profile.html', user_data=user_data)

@auth.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('student_id', None)
    session.pop('employer_id', None)
    session.pop('email', None)
    flash("Logged out successfully", category='success')
    return redirect(url_for('auth.login'))