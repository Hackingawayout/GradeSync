<!DOCTYPE html>
<html>
<head>
  <title>Display Students</title>
</head>
<body>
  <h1>Display Students</h1>
  <?php
    $host = "localhost";
    $user = "root";
    $password = "Arush_09";
    $database = "student_management";

    $connection = mysqli_connect($host, $user, $password, $database);

    if (!$connection) {
      die("Connection failed: " . mysqli_connect_error());
    }

    $query = "SELECT * FROM students";
    $result = mysqli_query($connection, $query);

    if (mysqli_num_rows($result) > 0) {
      echo "<table><tr><th>ID</th><th>Name</th><th>Grade</th></tr>";
      while($row = mysqli_fetch_assoc($result)) {
        echo "<tr><td>" . $row["id"]. "</td><td>" . $row["name"]. "</td><td>" . $row["grade"]. "</td></tr>";
      }
      echo "</table>";
    } else {
      echo "No students found";
    }

    mysqli_close($connection);
  ?>
</body>
</html>