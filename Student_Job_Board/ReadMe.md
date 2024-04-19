# Project Documentation

## GitHub Repository

- Utilize Git for tracking changes and feedback from the module leader.
- Link to the GitHub repo: [GitHub Repository](https://github.com/CS-LTU/com4003-summative-assessment-1-2314105)

## Discuss the use of cloud platforms such as Heroku or Azure for easy deployment and scaling

Using the cloud reduces the need of Infrastructure Management such as removing the need of physical hardware like servers, this allows the developers to not worry about the networking, or maintanence of hardware components/infustructure. By significantly reducing the burden on development teams allows them to focus more on building and improving their applications, which then allows for more scalability due to the reduced workload on developers. Cloud platforms also provide interfaces and tools that help with the deployment process which can begin to stream line the processes of deploying a web application. The cloud also provide services for tasks like database management, caching, monitoring, and security further which also adds to the general cost effectivnes and offloads the responsibilities from developers. Cloud platforms operate data centers globally, this provides a low-latency ecperience to users and offer content delivery networks (CDNs) for improved performance.

The student job board will have peak times of traffic mostly aimed aroung the term times of universities, this mean the web applocation should be able to handle spikes of traffic and be able to scale accordingly. Cloud based services allow for on demand scaling meaning in off peak times there may only be a small amount processing power being used to keep the website but once traffic starts to come more processing power and scalling will be applied allowing for the ocst effectivness of only paying for what you need. Comparing physical data structures to the cloud its easy to see the potential scalability the cloud can offer, especially if your complany can not affoard the infustructure of their own physical data centers, especially if you would like to one day globolize your app, the need for more physical data centeres would be required, but with the cloud they are already pre established allowing the ease of mind knowing that scalling is just a matter of software.

The cloud offers both vertical and horizontal scaling, along with auto-scaling, which is its standout feature. While vertical scaling remains similar, horizontal scaling benefits significantly from the cloud's ability to add or remove application instances seamlessly using virtual machines and functions. Auto-scaling stands out as a key advantage over physical data centers, allowing the cloud to adjust service scale based on demand. Cloud security aligns closely with physical data centers, it introduces additional layers such as end-to-end encryption and multi-factor authentication, enhancing data protection.

[1] [2] [3] [4]

### Project Goals and Objectives:

The primary goal of this project was to gain practical experience in backend development and implement my findings into a student job board, creating a full-scale web application with both backend and frontend components. The project aimed to be user-friendly and capable of executing SQL queries to interact with a MySQL database.

The project had two key objectives. Firstly, it aimed to understand backend development to determine the appropriate direction in building this application. This involved learning Flask, which was achieved through resources such as YouTube videos, Flask documentation, and example projects. MySQL was chosen for the database, leading to learning about SQL queries, including joiners. Flask and MySQL were selected due to their fast development compared to other platforms like Next.js, and because they were the primary languages being taught during the semester.

[7]

### Learning Objectives:

- Learn Flask
- Learn MySQL
- Understand basic data manipulation techniques
- Learn how to integrate backend and frontend components through middleware

### Project Objectives:

- Define the workflows for students, employers, and guests
- Determine the data to be fetched and displayed on each page
- Design one-to-many tables for students and employers
- Implement the directory based on Flask's documentation
- Create landing, login, and profile pages for both employers and students
- Implement password encryption for user security
- Develop edit profile pages for students and employers
- Utilize Flask sessions to store user data throughout the website
- Create base templates for inheritance and display flash messages
- Design and implement the employer job posting page and route
- Develop the student dashboard to display jobs posted by employers
- Implement search functionality for both students and employers
- Link the landing page to the "continue as guest" route
- Ensure web pages remain accessible even when the corresponding user is not in session
- Perform bug checking and ensure correct user flow and responsiveness of web pages

### Scope:

- Develop a web application for a Student Job Board using Bootstrap, Flask, and MySQL.
- Include features such as user authentication, job posting, job searching, student searching, and profile management.
- Design a responsive and user-friendly interface catering to students, employers, and guests.
- Utilize Flask for backend logic and MySQL for secure database interactions, incorporating password hashing for enhanced security.
- Follow a structured development process encompassing requirements gathering, design, implementation, and testing.
- Note: The project will not be deployed due to lack of access to cloud services.

## Installation Instructions

- Copy and paste the SQL from the student_job_board.sql into your MySQL Workbench; this will create the whole database.
- Check the init.py file and change the MySQL configurations to match your own.
- Press "CTRL" + "Shift" + " ' " to open your terminal.
- Copy and paste to create your virtual environment: py -3 -m venv .venv.
- To activate your virtual environment: .\.venv\Scripts\activate.
- Once activated, you should see a green (.venv) in your terminal.
- To install all dependencies: pip install -r requirements.txt.
- You now have everything ready; shut down your terminal and reopen as before.
- Activate your virtual environment: .\.venv\Scripts\activate.
- Run the application: python run.py.
- Control-click the link: http://127.0.0.1:5000.
- To prevent any directory issues, make sure the student_job_board folder is not inside any other folder.

## Basic Architecture

In this basic architecture, Flask acts as the middleware for our web application, using its lightweight and flexible framework for building web applications in Python and jinja. By using Flask with MySQL for data storage, Bootstrap for front-end design, and a live server for development feedback, this creates a system that connects the database with the user interface. Flask's routing system directs incoming requests to controller functions, where data processing and logic take place. Middleware functions handle tasks such as request parsing and authentication, ensuring smooth communication between the different components of the application. This architecture enables development and deployment of web applications with Flask, creating both functionality and user experience/responsive web pages.

## Technologies Used:

- HTML
- CSS
- JavaScript
- Python
- Jinja
- Flask
- MySQL
- Bootstrap
- live server

## Benefits:

- **Flexibility**: The modular architecture of Flask allows for easy integration with other Python libraries and extensions, enabling developers to customize and extend functionality as needed.

- **Scalability**: By separating concerns and following best practices in software design, the application architecture can accommodate future enhancements and scalability requirements.

- **Performance**: Flask's lightweight design and efficient request handling make it suitable for building high-performance web applications, delivering a responsive user experience.

- **Maintainability**: The use of well-established frameworks like Flask and Bootstrap, along with structured database management with MySQL, promotes code maintainability and facilitates collaborative development efforts.

## Next Steps:

In future iterations of the project, considerations for enhancing security measures, optimizing database performance, and implementing additional features to meet user requirements will be explored. Continuous refinement and iteration based on user feedback and technological advancements will drive the evolution of the application architecture.

## Legal and Ethical Considerations

The student job board will need to adhere to the data protection act making sure that both the students and employers' data is protected, this will be done with the use of hashing and a secret key. As this website is based in the UK, there is no need to follow outside regulations, allowing for an easier approach compared to other job board related websites. A terms and services will need to be obvious to the user when signing up, this will essentially show what the user is agreeing to when giving us their data. Equal opportunity for employers and students should be clear, this will be done by not allowing employers to discriminate on their job posting which will be moderated if the application was to be deployed. Employers should be screened beforehand to make sure no scammers are being allowed on the site; students are already screened as they are using their educational email. For future implementation, having accessibility features for the blind or other disabilities would be good to expand on.

[5] [6]

## Risk Assessment

Every website entails inherent risks, foremost among them being security vulnerabilities. These vulnerabilities, which may result in data breaches or unauthorized access to sensitive information, are a significant concern. Integrating hashing into the authentication system provides an additional layer of security for student and employer profiles. By storing only encrypted passwords, the risk of compromise in the event of a data breach is mitigated.

Server downtime and technical issues represent ongoing risks for most websites. To address this, regular code checks and improvements post-deployment are essential. Hosting the site on a cloud server offers added security and scalability benefits, as cloud servers are less prone to downtime and can easily handle fluctuations in site traffic.

The threat of hackers is another common risk factor in web application development. Regular software checks can help mitigate this risk, and implementing measures to prevent bot attacks, such as CAPTCHA or honeypot methods, further enhances security.

By acknowledging these risks and implementing appropriate mitigation strategies, such as robust authentication, cloud hosting, and anti-bot measures, the student job board can operate with greater security. Regular monitoring and updates will further bolster the platform's defenses against potential threats.

## Future Considerations for Scaling

As mentioned earlier, the cloud would be an ideal location to deploy the student job board in relation to scalability, especially during university term times when the site's traffic would ramp up. Cloud services would also reduce the cost of scaling; only the subscription price would be needed to deploy the site, eliminating expenses on building hardware, maintenance, or globalizing. If the student job board was successful, it would be ideal to globalize it and have it work in other countries, adjusting results based on the user's location.

## Project Plan & Reflection

![alt text](<READme images/Screenshot 2024-04-09 004333.png>)

### ERD

![ERD](<READme images/ERD.png>)

### Milestones

Throughout the front end and backend development, there were numerous milestones, for the front end:

- Learning the fundamentals of web development
- Getting the first webpage loaded with live server
- Using bootstrap
- Linking all the pages
- Finding SVG images making the pages more presentable

Backend:

- Learning how to set up a database
- Learning how to use Flask
- Re-creating all of my front end to accommodate the forms
- Using routes to link pages and passing user session data
- Connecting the database to the frontend with middleware (Flask)
- Re-creating the Gantt chart based on feedback
- Using the terminal more efficiently
- Understanding directories and the use of init files

### Reflection

My project planning for the backend development was poor. I misunderstood a lot of the database and middleware information and started to try different tech stacks such as MERN or using SQLAlchemy. Eventually, I came back to using Flask and MySQL by following the documentation from Flask's website and figuring out how to extract the data from the forms.

As shown in my Gantt chart and milestones, I decided to redesign all of my frontend. This was to simplify it for myself. I would first create the webpage, e.g., student signup, list out all of the fields required for a student, then render the page using routes or auth, I would create a SQL query relating to the form and create a table, use Flask to link the fields to the database and extract the information. This was essentially my way of going about creating the backend of the student job board.

## References

[1] Danielsson, P., Postema, T., & Munir, H. (2021). Heroku-Based Innovative Platform for Web-Based Deployment in Product Development at Axis. IEEE Access, 9, 10805–10819. https://doi.org/10.1109/access.2021.3050255

[2] Data security in cloud computing using AES under HEROKU cloud. (n.d.). Ieeexplore.ieee.org. https://ieeexplore.ieee.org/abstract/document/8372705

[3] RoseHJM. (2023, November 15). What is Azure Deployment Environments? - Azure Deployment Environments. Learn.microsoft.com. https://learn.microsoft.com/en-us/azure/deployment-environments/overview-what-is-azure-deployment-environments

[4] Jacek Cała, & Watson, P. (2010). Automatic Software Deployment in the Azure Cloud. Lecture Notes in Computer Science, 155–168. https://doi.org/10.1007/978-3-642-13645-0_12

[5] Government of UK. (2018). Data Protection. Gov.UK; www.gov.uk. https://www.gov.uk/data-protection#:~:text=The%20Data%20Protection%20Act%202018%20is%20the%20UK

[6] UK Government. (2010). Equality Act 2010. Legislation.gov.uk; Gov.uk. https://www.legislation.gov.uk/ukpga/2010/15/contents

[7] Flask. (2010). Welcome to Flask — Flask Documentation (2.3.x). Flask.palletsprojects.com. https://flask.palletsprojects.com/en/2.3.x/
