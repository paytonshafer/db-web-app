# Universty database web application
This app is a web application that allows users to examine a university database. There are 3 types of users: admin, instructor, and student. Upon reaching
the landing page, the user is prompted to login using their known login credentials. After they login their input is processed and if they are a authenticated
user they are lead to the proper page based on their group. There is a page for the admin user, instructors and students. On their respective page they are
given 1 to 3 options of queries to run so that they can get data from the database. The User Manuel which gives a detailed description of how to use the app is encluded above in the repo. We also have a design manuel which contains details on the design of the application as well as a ER-diragram and a schema of the university database.

# Installation and Usage
Ensure that you have Python installed, and then use pip to ensure that you have django and mysql-connector-python installed. Once you ensure those are 
installed you can download the source code and cd into the univerity directory. Now run the following command to start the server:
```sh
python3 manage.py runserver
```
Once the server has been started it can be found at http://127.0.0.1:8000, with the landing page of the app is located at http://127.0.0.1:8000/univdb

# Authors
Payton Shafer, Logan Paradas, Joshua To, and Jeffrey Donahue
