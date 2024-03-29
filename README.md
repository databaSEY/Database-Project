# Motorsports Database Mnagement System 
This project is developed by:  
[Eda Işık](https://github.com/isikeda)  
[Semih Gençten](https://github.com/semihgencten)  
[Yasin İbiş](https://github.com/yasinibis)  
for Database Course BLG317E

Welcome to our Flask-based web application for the Database class! Our project represents a comprehensive system designed to seamlessly integrate SQL functionality, catering to the management of information related to drivers, constructors, and races in the exciting realm of motorsports.

## Project Overview 
The user interface of our application offers dynamic pages for each category, providing users with an immersive experience for efficient search operations and access to detailed information on individual drivers, constructors, and races. With a user-friendly design, our application empowers users to effortlessly explore and analyze motorsports data.  

The web application is developed by flask without using any ORM. SQLite3 is used as database and we inserted our pure SQL queries into python code.

##  How to run
When you install the required libraires as shown in reauirements.txt you can use the following command to run the project: 
flask --app project run --debug

Then you can go to the link which is printed on terminal.


### Home page 
<div align="center">
  <img src="https://github.com/databaSEY/Database-Project/blob/main/images/home_page.png" alt="home">
  <p>Home Page</p>
</div>

This is our home page, it presents a brief information about core entities of our database.
As you can see admin can make Log In and Log Out operations to make sensitive Create, Update and Delete operations.

### Drivers, Constructors and Races Pages
These pages allow the user to list the records, search for the records and filter them.
They also allows admin to create new records, update existing ones and delete them.
There are also seperate detials pages for drivers and constructor pages to show detailed information about related entities.
Details of races are shown by a elegant design with an extendible part.

<div align="center">
  <img src="https://github.com/databaSEY/Database-Project/blob/main/images/constructors.png" alt="Constructor">
  <p>Constructor Page</p>
</div>

Allows the user to search by name, filter by nationality. Also implements pagination for an easy to use interface.  


<div align="center">
  <img src="https://github.com/databaSEY/Database-Project/blob/main/images/driver_page_create.png" alt="driver">
  <p>Driver Page's Create Section at the Bottom</p>
</div>

When the admin is logged in, she can make Create, Update and Delete operations on all of the pages.

<div align="center">
  <img src="https://github.com/databaSEY/Database-Project/blob/main/images/races.png" alt="Races">
  <p>Races page with details Part</p>
</div>

Shows the details of races with an elegant design.




