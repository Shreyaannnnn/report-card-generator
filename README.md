# report-card-generator

The goal of this project is to create a Report Card Management System application to manage report cards and export them with ease. 
Front-end for the program is written in Python, which also interacts with MySQL Server in the back-end. The program uses a Command-Line Interface to provide a menu-driven interactive access through a shell.

Third-party Python packages used:
Pillow  - provides powerful image processing capabilities
mysql-connector-python  - MySQL driver written in Python
xlrd  - library for reading and formatting information from Excel files

Features:
Show available classes  - Shows all classes for which grades are available
Find Record  - prints details of a record of one student/class
Export Card to .png file  - accesses data of student/class from database, formats it using Montserrat font onto a report card template named ‘card.png’, and saves a new .png file
Update Record  -  updates a single record
Delete Record  - deletes record of a student/class
Import data from .xlsx file  - reads records of a class from an Excel file and inserts them in the database

Program has 2 user modes:
Teacher   -  password-protected account with administrative privileges 
Student   -  minimal privileges to find and export their own record 
