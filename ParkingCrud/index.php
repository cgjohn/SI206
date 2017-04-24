<?php
require_once "pdo.php";
session_start();
?>
<html>
<head>
  <title>Connor Johnston</title>
</head>
<body>
<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
<link rel='stylesheet' type='text/css' href='//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css'>
 <div class="container">
<h1>Welcome to the parking Database</h1>
<?php
if ( isset($_SESSION['error']) ) {
  echo '<p style="color:red">'.$_SESSION['error']."</p>\n";
  unset($_SESSION['error']);
}
if ( isset($_SESSION['success']) ) {
  echo '<p style="color:green">'.$_SESSION['success']."</p>\n";
  unset($_SESSION['success']);
}
if ( isset($_SESSION['adding']) ) {
  echo '<p style="color:green">'.$_SESSION['adding']."</p>\n";
  unset($_SESSION['adding']);
}

if (!isset($_SESSION["email"]) ) { ?>
       <p><a href="login.php">Please log in</a> </p>
    <?php } 
else { ?>
 
    <?php echo('<table border="1">'."\n");


    $stmt = $pdo->query("SELECT parking_id, name, lot, price, spaces FROM parking");
    while ( $row = $stmt->fetch(PDO::FETCH_ASSOC) ) {
      echo "<tr><td>";
      echo(htmlentities($row['name']));
      echo("</td><td>");
      echo(htmlentities($row['lot']));
      echo("</td><td>");
      echo(htmlentities($row['price']));
      echo("</td><td>");
      echo(htmlentities($row['spaces']));
      echo("</td><td>");
      echo('<a href="edit.php?parking_id='.htmlentities($row['parking_id']).'">Edit</a> / ');
      echo('<a href="delete.php?parking_id='.htmlentities($row['parking_id']).'">Delete</a>');
      echo("</td></tr>\n");
    }
    ?>
  </table>
  <div><a href="add.php">Add New Entry</a></div>
  <a href="logout.php">Logout</a>

  

<?php } ?>

  </div>
</body>
</html>