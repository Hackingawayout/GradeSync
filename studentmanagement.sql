CREATE DATABASE student_management;
USE student_management;
CREATE TABLE students(
	 name VARCHAR (50),
     grade INT
     );

INSERT INTO students(name,grade)
VALUES
("AAA",91)
;

SELECT * FROM students;
DROP DATABASE student_management;
