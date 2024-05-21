import mysql.connector
from mysql.connector import Error

# Replace these values with your own database credentials
host = "localhost"
user = "root"
password = "Arush_09"
database = "student_management"

try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    if connection.is_connected():
        print("Successfully connected to the database")
        cursor = connection.cursor()     
        
    print("Welcome to GradeSync")
    while True:
        print("1. Add Student\n2. Display All Students\n3. Calculate Class Average Grade\n4. Exit\n")
        print("Enter your choice")
        choice = int(input())
        if choice == 1:
                name = input("Enter the name of the student: ")
                grade = int(input("Enter the grade of the students: "))
                try :
                    insertStudentRecord = "INSERT INTO students(name,grade) VALUES (%s,%s);"
                    cursor.execute(insertStudentRecord,(name,grade))
                    connection.commit()   
                    print("Student record added successfully.")                 
                except Error as e:
                    print(f"The error '{e}' occured")
                
                
        elif choice == 2:
            print("\nHere is a list of the students:\n")
            try:
                showData = "SELECT * FROM students"
                cursor.execute(showData)
                student = cursor.fetchall()
                for stu in student:
                    print(stu)
            except Error as e:
                print(f"The error '{e} occured")
                
        elif choice == 3:
            try:
                cursor.execute("SELECT AVG(grade) FROM students")
                average_grade = cursor.fetchone()[0]
                if average_grade is None:
                    print("No students in the list.")
                else:
                    print(f"Class Average Grade: {average_grade}")
            except Error as e:
                print(f"The error '{e} occured") 
            
        elif choice == 4:
            exit()
            
        else:
            print("Invalid choice")
            

except mysql.connector.Error as err:
    print(f"Error: {err}")
