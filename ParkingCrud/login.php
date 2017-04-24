<?php // Do not put any HTML above this line

if ( isset($_POST['cancel'] ) ) {
    // Redirect the browser to game.php
    header("Location: index.php");
    return;
}

$salt = 'XyZzy12*_';
$stored_hash = '1a52e17fa899cf40fb04cfc42e6352f1';  // Pw is meow123

$failure = false;  // If we have no POST data

// Check to see if we have some POST data, if we do process it
session_start();
if ( isset($_POST['email']) && isset($_POST['pass']) ) {
    if ( strlen($_POST['email']) < 1 || strlen($_POST['pass']) < 1 ) {
        $failure = "User name and password are required";
        $_SESSION["error"] = "User name and password are required"; 
    } 
    elseif (strpos($_POST['email'], '@') === false ) {
       $failure = "Email must have an at-sign (@)";
    }
    else {
        unset($_SESSION["email"]);
        $check = hash('md5', $salt.$_POST['pass']);
        if ( $check == $stored_hash ) {
            $_SESSION["email"] = $_POST["email"];
            $_SESSION["success"] = "Logged in.";
            header( 'Location: index.php' ) ;
            return;
            error_log("Login success ".$_POST['email']);
            header("Location: index.php");
            return;
        } 
        else {
          $_SESSION["error"] = "Incorrect password.";
            error_log("Login fail ".$_POST['email']." $check");
            header('Location: login.php'); 
            $failure = "Incorrect password";
            return;
        }
    }
}

// Fall through into the View
?>
<!DOCTYPE html>
<html>
<head>
<title>Connor Johnston</title>
</head>
<body>
  <div class="container">
    <h1>Please Log In</h1>

    <?php
      if ( isset($_SESSION["error"]) ) {
          echo('<p style="color:red">'.$_SESSION["error"]."</p>\n");
          unset($_SESSION["error"]);
      }
    ?> 

    <form method="POST">
      <label for="nam">User Name</label>
      <input type="text" name="email" id="nam"><br/>
      <label for="id_1723">Password</label>
      <input type="text" name="pass" id="id_1723"><br/>
      <input type="submit" value="Log In">
      <input type="submit" name="cancel" value="Cancel">
    </form>

  </div>
</body>
