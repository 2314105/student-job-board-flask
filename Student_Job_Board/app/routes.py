
from app import app, mysql
from flask import render_template, session, redirect, url_for, flash, request, send_from_directory
from app.auth import auth
import os
from werkzeug.utils import secure_filename

# Define the uploads directory
UPLOAD_FOLDER = 'app/static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def landing_page():
    return render_template('landing_page.html')
#app.register_blueprint(auth)

@app.route('/landing-page')
def landing_page_redirect():
    return render_template('landing_page.html')

@app.route('/student-dashboard')
def student_dashboard():
    if 'loggedin' in session and 'student_id' or 'guest' in session:
        cur = mysql.connection.cursor()

        # Check if a search query was provided
        search_query = request.args.get('q')

        if search_query:
            # Modified SQL query to retrieve filtered job listings based on search query
            cur.execute("""
                SELECT ej.id, ej.title, ej.description, ej.requirements, ej.location, ej.job_type, ej.salary, ej.employer_id, GROUP_CONCAT(js.skill_name) AS skills
                FROM employer_job AS ej
                LEFT JOIN (SELECT employer_job_id, GROUP_CONCAT(skill_name) AS skill_name
                           FROM job_skills
                           GROUP BY employer_job_id) AS js ON ej.id = js.employer_job_id
                WHERE js.skill_name LIKE %s
                GROUP BY ej.id;
            """, ('%' + search_query + '%',))
        else:
            # Default SQL query to retrieve all job listings
            cur.execute("""
                SELECT ej.id, ej.title, ej.description, ej.requirements, ej.location, ej.job_type, ej.salary, ej.employer_id, GROUP_CONCAT(js.skill_name) AS skills
                FROM employer_job AS ej
                LEFT JOIN (SELECT employer_job_id, GROUP_CONCAT(skill_name) AS skill_name
                           FROM job_skills
                           GROUP BY employer_job_id) AS js ON ej.id = js.employer_job_id
                GROUP BY ej.id;
            """)

        # Process fetched data
        jobs = []
        for row in cur.fetchall():
            job = {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'requirements': row[3],
                'location': row[4],
                'job_type': row[5],
                'salary': row[6],
                'employer_id': row[7],
                'skills': row[8].split(',') if row[8] else []  # Split skills string into a list
            }
            jobs.append(job)

        cur.close()

        # Pass processed data to template for rendering
        return render_template('student_dashboard.html', jobs=jobs)
    else:
        flash("You are not logged in", category='error')
        return redirect(url_for('auth.login'))


@app.route('/student-profile')
def student_profile():
    if 'loggedin' in session:
        if 'student_id' in session:
            # If logged in as a student, get student ID from session
            user_id = session['student_id']
        elif 'employer_id' or 'guest' in session:
            # If logged in as an employer, retrieve student ID from URL parameters
            user_id = request.args.get('student_id')
            if not user_id:
                flash("Student ID is required", category='error')
                return redirect(url_for('employer_dashboard'))
        else:
            flash("You are not logged in", category='error')
            return redirect(url_for('auth.login'))

        cur = mysql.connection.cursor()

        # Fetch the student's basic information
        cur.execute("SELECT * FROM student WHERE student_id = %s", (user_id,))
        user = cur.fetchone()

        if user:
            # Fetch the student's contact information
            cur.execute("SELECT * FROM student_contact WHERE student_id = %s", (user_id,))
            contact = cur.fetchone()
            # Fetch the student's work experience
            cur.execute("SELECT * FROM student_work_experience WHERE student_id = %s", (user_id,))
            work_experience = cur.fetchall()

            # Fetch the student's education
            cur.execute("SELECT * FROM student_education WHERE student_id = %s", (user_id,))
            education = cur.fetchall()

            # Fetch the student's skills
            cur.execute("SELECT skill_name FROM student_key_skills WHERE student_id = %s", (user_id,))
            skills = [row[0] for row in cur.fetchall()]  # Extract skills from result

            cur.close()

            return render_template('student_profile.html', user=user, work_experience=work_experience, education=education, skills=skills, contact=contact)
        else:
            flash("User not found", category='error')
            return redirect(url_for('auth.login'))
    else:
        flash("You are not logged in", category='error')
        return redirect(url_for('auth.login'))


    

@app.route('/student-work-experience', methods=['GET', 'POST'])
def student_work_experience():
    if 'student_id' not in session:
        flash('You need to be logged in as a student to add work experience', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # Extract form data
        company = request.form['company']
        position = request.form['position']
        duration_year = request.form['year']
        duration_month = request.form['month']
        responsibility = request.form['responsibility']
        student_id = session['student_id']

        # Insert work experience data into the database
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO student_work_experience (student_id, company, position, duration_year, duration_month, responsibility)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (student_id, company, position, duration_year, duration_month, responsibility))
        
        mysql.connection.commit()
        cur.close()

        flash('Work experience added successfully', 'success')
        return redirect(url_for('student_profile'))

    return render_template('student_work_experience.html')

@app.route('/student-education', methods=['GET', 'POST'])
def student_edication():
    if 'student_id' not in session:
        flash('You need to be logged in as a student to add an education', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # Extract form data
        institution = request.form['institution']
        field_of_study = request.form['study']
        degree = request.form['degree']
        years_attended = request.form['year']
        student_id = session['student_id']

        # Insert education data into the database
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO student_education (student_id, institution, field_of_study, degree, years_attended)
            VALUES (%s, %s, %s, %s, %s)
        """, (student_id, institution, field_of_study, degree, years_attended))
        
        mysql.connection.commit()
        cur.close()

        flash('Education added successfully', 'success')
        return redirect(url_for('student_profile'))

    return render_template('student_education.html')

# Route for updating student profile picture
@app.route('/student-profile-picture', methods=['POST'])
def student_profile_picture():
    # Check if user is logged in as a student
    if 'student_id' not in session:
        flash('You need to be logged in as a student to add an education', 'error')
        return redirect(url_for('auth.login'))
    
    # Get uploaded profile picture from the request
    profile_picture = request.files['profile_picture']
    
    # Check if a file was selected
    if profile_picture.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)
    
    # Securely save the uploaded file
    filename = secure_filename(profile_picture.filename)
    profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    # Update student's profile picture in the database
    cur = mysql.connection.cursor()
    cur.execute("UPDATE student SET profile_picture = %s WHERE student_id = %s", (filename, session['student_id']))
    mysql.connection.commit()
    cur.close()
    
    # Flash success message
    flash('Profile picture uploaded successfully', 'success')
    
    # Redirect to the student profile page
    return redirect(url_for('student_profile'))

# Route for managing student key skills
@app.route('/student-key-skills', methods=['GET', 'POST'])
def student_key_skills():
    # Check if user is logged in as a student
    if 'student_id' not in session:
        flash('You need to be logged in as a student to add key skills', 'error')
        return redirect(url_for('auth.login'))

    # Check if form is submitted via POST method
    if request.method == 'POST':
        # Extract key skills from form data
        skills_string = request.form['skills']
        student_id = session['student_id']

        # Split the skills string by commas to get individual skills
        skills = [skill.strip() for skill in skills_string.split(',')]

        # Insert each skill into the student_key_skills table
        cur = mysql.connection.cursor()
        for skill_name in skills:
            cur.execute("""
                INSERT INTO student_key_skills (student_id, skill_name)
                VALUES (%s, %s)
            """, (student_id, skill_name))
        
        # Commit changes to the database and close cursor
        mysql.connection.commit()
        cur.close()

        # Flash success message and redirect to student profile
        flash('Key skills added successfully', 'success')
        return redirect(url_for('student_profile'))
    
    # Render the student key skills template for GET requests
    return render_template('student_key_skills.html')

# Route for deleting work experience
@app.route('/delete-work-experience/<int:exp_id>', methods=['GET','POST'])
def delete_work_experience(exp_id):
    # Check if user is logged in and is a student
    if 'loggedin' in session and 'student_id' in session:
        user_id = session['student_id']
        
        # Check if the logged-in user owns the work experience entry
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student_work_experience WHERE id = %s AND student_id = %s", (exp_id, user_id))
        exp = cur.fetchone()
        
        if exp:
            # Delete the work experience entry from the database
            cur.execute("DELETE FROM student_work_experience WHERE id = %s", (exp_id,))
            mysql.connection.commit()
            cur.close()
            flash("Work experience deleted successfully", category='success')
        else:
            flash("Unauthorized access or work experience not found", category='error')
        
        return redirect(url_for('student_profile'))
    else:
        flash("You are not logged in", category='error')
        return redirect(url_for('auth.login'))

# Route for deleting education entry
@app.route('/delete-education/<int:edu_id>', methods=['GET','POST'])
def delete_education(edu_id):
    # Check if user is logged in and is a student
    if 'loggedin' in session and 'student_id' in session:
        user_id = session['student_id']
        
        # Check if the logged-in user owns the education entry
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student_education WHERE id = %s AND student_id = %s", (edu_id, user_id))
        edu = cur.fetchone()
        
        if edu:
            # Delete the education entry from the database
            cur.execute("DELETE FROM student_education WHERE id = %s", (edu_id,))
            mysql.connection.commit()
            cur.close()
            flash("Education entry deleted successfully", category='success')
        else:
            flash("Unauthorized access or education entry not found", category='error')
        
        return redirect(url_for('student_profile'))
    else:
        flash("You are not logged in", category='error')
        return redirect(url_for('auth.login'))
    
# Route for deleting profile picture
@app.route('/delete-profile-picture', methods=['POST'])
def delete_profile_picture():
    # Check if the user is logged in as a student or employer
    if 'loggedin' in session:
        user_id = session.get('student_id') or session.get('employer_id')
        profile_picture_column = 'profile_picture'

        if 'student_id' in session:
            table_name = 'student'
        elif 'employer_id' in session:
            table_name = 'employer'
        else:
            flash("Invalid user type", category='error')
            return redirect(url_for('index'))

        cur = mysql.connection.cursor()
        
        # Fetch the user's current profile picture
        cur.execute(f"SELECT {profile_picture_column} FROM {table_name} WHERE {table_name}_id = %s", (user_id,))
        profile_picture = cur.fetchone()[0]
        
        # Delete the photo file from the folder
        if profile_picture:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_picture)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Update the database entry to remove the profile picture
        cur.execute(f"UPDATE {table_name} SET {profile_picture_column} = NULL WHERE {table_name}_id = %s", (user_id,))
        mysql.connection.commit()
        cur.close()
        
        flash("Profile picture deleted successfully", category='success')
    else:
        flash("You are not logged in", category='error')
    
    # Redirect based on user type
    if 'student_id' in session:
        return redirect(url_for('student_profile'))
    elif 'employer_id' in session:
        return redirect(url_for('employer_profile'))
    else:
        return redirect(url_for('index'))


# Route for deleting student's key skills
@app.route('/delete-student-key-skills', methods=['POST'])
def delete_student_key_skills():
    # Check if the user is logged in as a student
    if 'student_id' not in session:
        flash('You need to be logged in as a student to delete key skills', 'error')
        return redirect(url_for('auth.login'))

    # Check if the request method is POST
    if request.method == 'POST':
        student_id = session['student_id']

        # Delete all skills associated with the student from the database
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM student_key_skills WHERE student_id = %s", (student_id,))
        mysql.connection.commit()
        cur.close()

        flash('Key skills deleted successfully', 'success')
        return redirect(url_for('student_profile'))

    # If the request method is not POST, redirect to the student profile page
    return redirect(url_for('student_profile'))


#//////////////////////////////////////////////////
#//                                              //
#//                                              //
#//                                              //
#//                EMPLOYER ROUTES               //
#//                                              // 
#//                                              //
#//                                              //
#//////////////////////////////////////////////////

# Route for searching students
@app.route('/search-for-students', methods=['GET', 'POST'])
def search_for_students():
    # Check if the user is logged in as an employer
    if 'loggedin' in session and 'employer_id' or 'guest' in session:
        cur = mysql.connection.cursor()

        # Get search query parameters from URL
        search_query = request.args.get('q')  # Combined search query

        # Construct SQL query based on combined search parameter
        if search_query:
            sql_query = """
                SELECT 
                    s.student_id, 
                    s.forename, 
                    s.surname, 
                    se.field_of_study, 
                    se.degree, 
                    GROUP_CONCAT(ss.skill_name) AS skills
                FROM 
                    student AS s
                LEFT JOIN 
                    student_education AS se ON s.student_id = se.student_id
                LEFT JOIN 
                    (SELECT student_id, GROUP_CONCAT(skill_name) AS skill_name
                    FROM student_key_skills
                    GROUP BY student_id) AS ss ON s.student_id = ss.student_id
                WHERE 
                    se.field_of_study LIKE %s
                    OR se.degree LIKE %s
                    OR ss.skill_name LIKE %s
                GROUP BY 
                    s.student_id, s.forename, s.surname, se.field_of_study, se.degree;
            """
            # Execute the SQL query with placeholders for search_query
            cur.execute(sql_query, ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
        else:
            # If no search query provided, retrieve all students
            sql_query = """
                SELECT 
                    s.student_id, 
                    s.forename, 
                    s.surname, 
                    se.field_of_study, 
                    se.degree, 
                    GROUP_CONCAT(ss.skill_name) AS skills
                FROM 
                    student AS s
                LEFT JOIN 
                    student_education AS se ON s.student_id = se.student_id
                LEFT JOIN 
                    (SELECT student_id, GROUP_CONCAT(skill_name) AS skill_name
                    FROM student_key_skills
                    GROUP BY student_id) AS ss ON s.student_id = ss.student_id
                GROUP BY 
                    s.student_id, s.forename, s.surname, se.field_of_study, se.degree;
            """
            # Execute the default SQL query
            cur.execute(sql_query)

        # Process fetched data
        students = []
        for row in cur.fetchall():
            student = {
                'student_id': row[0],
                'forename': row[1],
                'surname': row[2],
                'field_of_study': row[3],
                'degree': row[4],
                'skills': row[5].split(',') if row[5] else []  # Split skills string into a list
            }
            students.append(student)

        cur.close()

        # Pass processed data to template for rendering
        return render_template('employer_search_students.html', students=students)
    else:
        flash("You are not logged in", category='error')
        return redirect(url_for('auth.login'))
    


# Route for displaying employer profile
@app.route('/employer-profile')
def employer_profile():
    if 'loggedin' in session:
        if 'employer_id' in session:
            # If logged in as an employer, get employer ID from session
            employer_id = session['employer_id']
        elif 'student_id' or 'guest' in session:
            # If logged in as a student, retrieve employer ID from URL parameters
            employer_id = request.args.get('employer_id')
            print("Employer ID from URL parameters:", employer_id) 
            if not employer_id:
                flash("Employer ID is required", category='error')
                return redirect(url_for('student_dashboard'))
        else:
            flash("You are not logged in", category='error')
            return redirect(url_for('auth.login'))

        cur = mysql.connection.cursor()

        # Fetch the employer's basic information
        cur.execute("SELECT * FROM employer WHERE employer_id = %s", (employer_id,))
        employer = cur.fetchone()

        if employer:
            # Fetch the jobs posted by this employer
            cur.execute("""
                SELECT ej.id, ej.title, ej.description, ej.requirements, ej.location, ej.job_type, ej.salary, GROUP_CONCAT(js.skill_name) AS skills
                FROM employer_job AS ej
                LEFT JOIN (SELECT employer_job_id, GROUP_CONCAT(skill_name) AS skill_name
                           FROM job_skills
                           GROUP BY employer_job_id) AS js ON ej.id = js.employer_job_id
                WHERE ej.employer_id = %s
                GROUP BY ej.id;
            """, (employer_id,))
            jobs = []
            for row in cur.fetchall():
                job = {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'requirements': row[3],
                    'location': row[4],
                    'job_type': row[5],
                    'salary': row[6],
                    'skills': row[7].split(',') if row[7] else []
                }
                jobs.append(job)
            cur.close()

            return render_template('employer_profile.html', employer=employer, jobs=jobs)
        else:
            flash("Employer not found", category='error')
            return redirect(url_for('auth.login'))
    else:
        flash("You are not logged in", category='error')
        return redirect(url_for('auth.login'))


# Route for uploading employer profile picture
@app.route('/employer-profile-picture', methods=['POST'])
def employer_profile_picture():
    if 'employer_id' not in session:
        flash('You need to be logged in as an employer to add a profile picture', 'error')
        return redirect(url_for('auth.login'))

    # Retrieve the uploaded profile picture file
    profile_picture = request.files['profile_picture']

    if profile_picture.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('employer_profile'))

    # Securely save the uploaded file
    filename = secure_filename(profile_picture.filename)
    profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Update the database with the new profile picture filename
    cur = mysql.connection.cursor()
    cur.execute("UPDATE employer SET profile_picture = %s WHERE employer_id = %s", (filename, session['employer_id']))
    mysql.connection.commit()
    cur.close()

    flash('Profile picture uploaded successfully', 'success')

    return redirect(url_for('employer_profile'))


# Route for creating a new job listing
@app.route('/job-listing', methods=['GET', 'POST'])
def job_listing():
    if request.method == 'POST':
        # Extract form data
        title = request.form['title']
        description = request.form['description']
        requirements = request.form['requirements']
        job_type = request.form['job_type']
        deadline_day = request.form['day']
        deadline_month = request.form['month']
        deadline_year = request.form['year']
        location = request.form['location']
        salary = request.form['salary']
        skills = request.form['skills']  # Change to single skill input field
        employer_id = session.get('employer_id')

        # Insert job listing into the database
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO employer_job (employer_id, title, description, requirements, job_type, deadline_day, deadline_month, deadline_year, location, salary)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (employer_id, title, description, requirements, job_type, deadline_day, deadline_month, deadline_year, location, salary))
        job_id = cur.lastrowid  # Get the ID of the inserted job listing

        # Split the skills string and insert each skill separately
        for skill_name in skills.split(','):
            cur.execute("INSERT INTO job_skills (employer_job_id, skill_name) VALUES (%s, %s)", (job_id, skill_name.strip(),))

        mysql.connection.commit()
        cur.close()

        flash('Job listing created successfully', 'success')
        return redirect(url_for('employer_profile'))
    # Render the job listing creation form
    return render_template('employer_job_listing.html')

# Route for deleting a job listing
@app.route('/delete-job', methods=['POST'])
def delete_job():
    if 'loggedin' in session and session['user_type'] == 'employer':
        # Check if the job_id is provided in the request
        if 'job_id' in request.form:
            job_id = request.form['job_id']
            cur = mysql.connection.cursor()
            
            # Delete the tags associated with the job listing
            cur.execute("DELETE FROM job_skills WHERE employer_job_id = %s", (job_id,))
            
            # Delete the job listing from the database
            cur.execute("DELETE FROM employer_job WHERE id = %s", (job_id,))
            mysql.connection.commit()
            cur.close()
            
            flash("Job listing deleted successfully", category='success')
        else:
            flash("Job ID not provided", category='error')
    else:
        flash("Unauthorized access", category='error')
    
    return redirect(url_for('employer_profile'))
