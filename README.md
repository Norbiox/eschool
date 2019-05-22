# eschool
This is a project of web application, prepared for schools, serves as:

* home page of school for visitors
* school register for teachers and students
* file sharing system for teachers and students


## Technology stack

* python
* Django
* SQLite


## Description

Project consists of 3 django applications described below.

This is a simplified relational database schema used in application:

![dbschema](https://raw.githubusercontent.com/Norbiox/eschool/master/school_book.png)


### Home

Serves as a home page of school for visitors.
Contains news page, school informations page and contact page.


### SchoolRegister

This application is meant to be used by logged in teachers and students only.
It allows to:

* search and view students and teachers informations
* view students presences on lessons, grades and notes
* manage lessons and students presences on thems (only for teachers)
* manage students grades and notes (like for bad behaviour) (only for teachers)

SchoolRegister has view restrictions.
Certain students informations like grades can be viewed only by owner or related teacher (who gave particular grade).


### FileShare

Application only for logged in teachers and students.
It allows them to upload and share small files (up to 10MB) between them.
E.g teacher can upload a homework paper and share with his students.

