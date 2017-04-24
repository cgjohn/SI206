<?php
require_once "pdo.php";
session_start();
if ( isset($_POST['name']) && isset($_POST['lot']) 
     && isset($_POST['price']) && isset($_POST['spaces']) && isset($_POST['parking_id']) ) {
     
    //Check if fields are empty
    if (empty($_POST['name']) || empty($_POST['lot']) || empty($_POST['price']) || empty($_POST['spaces']) ) {
      $_SESSION['error'] = 'All fields are required';
      header( 'Location: edit.php?parking_id='.htmlentities($_GET['parking_id'])) ;
      return;
    }
    //Check if price mile fields are numeric
    elseif (!is_numeric($_POST['price']) ) {
      $_SESSION['error'] = 'price must be an integer';
      header( 'Location: edit.php?parking_id='.htmlentities($_GET['parking_id'])) ;
      return;
    }
    elseif (!is_numeric($_POST['spaces']) ) {
      $_SESSION['error'] = 'spaces must be an integer';
      header( 'Location: edit.php?parking_id='.htmlentities($_GET['parking_id'])) ;
      return;
    }
    else {
    $sql = "UPDATE parking SET name = :name, 
            lot = :lot, price = :price, spaces = :spaces
            WHERE parking_id = :parking_id";
    $stmt = $pdo->prepare($sql);

    $stmt->execute(array(
        ':name' => $_POST['name'],
    		':lot' => $_POST['lot'],
    		':price' => $_POST['price'],
    		':spaces' => $_POST['spaces'],
        ':parking_id' => $_POST['parking_id']));

    $_SESSION['success'] = 'Record edited';
    header( 'Location: index.php' ) ;
    return;
    }
}

if ( isset($_SESSION['error']) ) {
  echo '<p style="color:red">'.$_SESSION['error']."</p>\n";
  unset($_SESSION['error']);
}

$stmt = $pdo->prepare("SELECT * FROM parking where parking_id = :abc");
$stmt->execute(array(":abc" => $_GET['parking_id']));
$row = $stmt->fetch(PDO::FETCH_ASSOC);
if ( $row === false ) {
    $_SESSION['error'] = 'Bad value for id';
    header( 'Location: index.php' ) ;
    return;
}
$nm = htmlentities($row['name']);
$lt = htmlentities($row['lot']);
$pr = htmlentities($row['price']);
$sp = htmlentities($row['spaces']);
$id = htmlentities($row['parking_id']);
?>

<p>Edit User</p>
<form method="post">
<p>name:
<input type="text" name="name" value="<?= $nm ?>"></p>
<p>lot:
<input type="text" name="lot" value="<?= $lt ?>"></p>
<p>price:
<input type="text" name="price" value="<?= $pr ?>"></p>
<p>spaces:
<input type="text" name="spaces" value="<?= $sp ?>"></p>
<input type="hidden" name="parking_id" value="<?= $id ?>">
<p><input type="submit" value="Save"/>
<a href="index.php">Cancel</a></p>



