<?php
require_once "pdo.php";
session_start();
if ( isset($_POST['parking_id']) ) {
	$sql = "DELETE FROM parking WHERE parking_id = :zip";
	$stmt = $pdo->prepare($sql);
	$stmt->execute(array(':zip' => $_POST['parking_id']));
	$_SESSION['success'] = 'Record deleted';
	header( 'Location: index.php' ) ;
	return;
}
$stmt = $pdo->prepare("SELECT parking_id, name FROM parking where parking_id = :xyz");
$stmt->execute(array(":xyz" => $_GET['parking_id']));
$row = $stmt->fetch(PDO::FETCH_ASSOC);
if ( $row === false ) {
	$_SESSION['error'] = 'Bad value for id';
	header( 'Location: index.php' ) ;
	return;
}
echo "<p>Confirm: Deleting ".htmlentities($row['name'])."</p>\n";
echo('<form method="post"><input type="hidden" ');
echo('name="parking_id" value="'.$row['parking_id'].'">'."\n");
echo('<input type="submit" value="Delete" name="delete">');
echo('<a href="index.php">Cancel</a>');
echo("\n</form>\n");
?>
