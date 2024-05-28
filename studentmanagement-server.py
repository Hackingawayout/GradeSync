import mysql.connector
from mysql.connector import Error
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import simplejson as json
import datetime

#log
def log(str1):
    current_date = datetime.date.today()
    current_time = datetime.datetime.now().time()
    with open("Log-server.txt","a") as f:
        f.write(f"{str1} at {current_time} on {current_date}\n")

# Database credentials
host = "localhost"
user = "root"
password = "Arush_09"
database = "student_management"

# Establish database connection
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            log("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None

# Define the request handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        connection = connect_to_db()
        log("Connection of server to database was sucessful.")
        if not connection:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Database connection failed'}).encode('utf-8'))
            log("Connection of server to database failed.")
            return
            
            
        cursor = connection.cursor()

        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        print(f"Query_params:{query_params}")

        if path == "/display_students":
            try:
                student_id = query_params["id"][0]
                print(student_id)
                
                if student_id:
                    student_indi_display = "SELECT * FROM students WHERE id=%s"
                    cursor.execute(student_indi_display,[student_id])
                else:
                    cursor.execute("SELECT * FROM students")
                students = cursor.fetchall()
                for stu in students:
                    print(stu)
                students_list = [{'id': stu[0], 'name': stu[1], 'grade': stu[2]} for stu in students]
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(students_list).encode('utf-8'))
            except Error as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

        elif path == "/class_average":
            try:
                cursor.execute("SELECT AVG(grade) FROM students")
                average_grade = cursor.fetchone()[0]
                if average_grade is None:
                    average_grade = 0
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'average_grade': average_grade}).encode('utf-8'))
            except Error as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not Found'}).encode('utf-8'))

        cursor.close()
        connection.close()

    def do_POST(self):
        connection = connect_to_db()
        if not connection:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Database connection failed'}).encode('utf-8'))
            return

        cursor = connection.cursor()

        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/add_student":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_json_data = json.loads(post_data.decode('utf-8'))
            print(post_json_data)

            name = post_json_data["name"]
            grade = post_json_data["grade"]

            if name and grade:
                try:
                    insertStudentRecord = "INSERT INTO students(name, grade) VALUES (%s, %s)"
                    cursor.execute(insertStudentRecord, (name, int(grade)))
                    connection.commit()
                    self.send_response(201)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'message': 'Student record added successfully'}).encode('utf-8'))
                except Error as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid input'}).encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not Found'}).encode('utf-8'))

        cursor.close()
        connection.close()

# Set up and start the server
def run_server():
    host = 'localhost'
    port = 8080
    # Create an instance of HTTPServer with our handler class
    server = HTTPServer((host, port), RequestHandler)
    '''server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, RequestHandler)'''
    print(f"Server started at http://{host}:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
