<!DOCTYPE html>
<html>
<head>
  <title>Add Student</title>
</head>
<body>
  <h1>Add Student</h1>
  <?php
    $host = "localhost";
    $user = "root";
    $password = "Arush_09";
    $database = "student_management";

    if ($_SERVER["REQUEST_METHOD"] == "POST") {
      $id = $_POST["id"];
      $name = $_POST["name"];
      $grade = $_POST["grade"];

      $connection = mysqli_connect($host, $user, $password, $database);

      if (!$connection) {
        die("Connection failed: " . mysqli_connect_error());
      }

      $query = "INSERT INTO students (id,name, grade) VALUES ('$id','$name', '$grade')";
      $result = mysqli_query($connection, $query);

      if ($result) {
        echo "<p>Student added successfully</p>";
      } else {
        echo "<p>Error adding student: " . mysqli_error($connection) . "</p>";
      }

      mysqli_close($connection);
    }
  ?>
  <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
    <label for="id">Grade:</label><br>
    <input type="number" id="id" name="id"><br>
    <label for="name">Name:</label><br>
    <input type="text" id="name" name="name"><br>
    <label for="grade">Grade:</label><br>
    <input type="number" id="grade" name="grade"><br>
    <input type="submit" value="Submit">
  </form>
</body>
</html>