<?php
require_once "pdo.php";
session_start();

if ( ! isset($_SESSION['email']) ) {
  die('Not logged in');
}

if ( isset($_POST['logout']) ) {
    header('Location: index.php');
    return;
}

$failure = false;

if ( isset($_POST['adding'] ) ) {
  if( strlen($_POST['name']) < 1 || strlen($_POST['lot']) < 1 || strlen($_POST['price']) < 1  || strlen($_POST['spaces']) < 1  ){ 
    // $failure = "name is required"; 
    $_SESSION['error'] = "All fields are required"; 
    header( 'Location: add.php' ) ;
    return;
  } 
  else {
    if(!(is_numeric($_POST['price'])) ){ 
      // $failure = "spaces and price must be numeric";
      $_SESSION['error'] = "price must be an integer";
      header( 'Location: add.php' ) ;
      return;
    }
    if(!(is_numeric($_POST['spaces'])) ){ 
      // $failure = "spaces and price must be numeric";
      $_SESSION['error'] = "spaces must be an integer";
      header( 'Location: add.php' ) ;
      return;
    }
   
    else{ 
      $_SESSION['adding'] = "Record added";

      $stmt = $pdo->prepare('INSERT INTO parking(name, price, lot, spaces) VALUES ( :nm, :pr, :lt, :sp)');
        $stmt->execute(array(
            ':nm' => $_POST['name'],
            ':pr' => $_POST['price'],
            ':lt' => $_POST['lot'],
            ':sp' => $_POST['spaces'])
        );

      header("Location: index.php");
      $failure="hi";
      return;

    }
  }
 
} 
?>

<?php
  if ( isset($_SESSION["error"]) ) {
      echo('<p style="color:red">'.$_SESSION["error"]."</p>\n");
      unset($_SESSION["error"]);
  }
?> 


<form method="POST">
<label for="name_id">name</label>
<input type="text" name="name" id="name_id"><br/>
<label for="lot_id">lot</label>
<input type="text" name="lot" id="lot_id"><br/>
<label for="price_id">price</label>
<input type="text" name="price" id="price_id"><br/>
<label for="spaces_id">spaces</label>
<input type="text" name="spaces" id="spaces_id"><br/>
<input type="submit" value="Add" name="adding">
</form>