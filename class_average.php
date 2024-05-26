<!DOCTYPE html>
<html>
<head>
  <title>Class Average</title>
</head>
<body>
  <h1>Class Average</h1>
  <?php
    $host = "localhost";
    $user = "root";
    $password = "Arush_09";
    $database = "student_management";

    $connection = mysqli_connect($host, $user, $password, $database);

    if (!$connection) {
      die("Connection failed: " . mysqli_connect_error());
    }

    $query = "SELECT AVG(grade) FROM students";
    $result = mysqli_query($connection, $query);

    if (mysqli_num_rows($result) > 0) {
      $row = mysqli_fetch_assoc($result);
      echo "<p>Class Average: " . $row["AVG(grade)"] . "</p>";
    } else {
      echo "No students found";
    }

    mysqli_close($connection);
  ?>
</body>
</html>