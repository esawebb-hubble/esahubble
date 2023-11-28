<?

$mailto 	= trim($_POST['SPACEmailto']);
$redirect 	= trim($_POST['SPACEredirect']);
$subject 	= trim($_POST['SPACEsubject']);
$fields 	= $_POST['SPACEfields'];

// Check mailto
$mailval = explode('@', $mailto);

if (!(count($mailval) == 2 && ($mailval[1] == 'hankat.dk') or ($mailval[1] == 'eso.org') or ($mailval[1] == 'spacetelescope.org'))) {
	reportError("Invalid mail-to address");
}

if (get_magic_quotes_gpc()) {
	$fields = stripcslashes(stripslashes($fields)); 
} 

// SECURITY WARNING
//
// DO NOT USE $fields IN DYNMAIC STRINGS!!!!!!!!!!! 

if (!preg_match_all('/ID_([a-z_]+)/', $fields, $fieldsArray)){
	reportError('No fields defined');
}

for ($i = 0; $i < count($fieldsArray[0]); $i++) {
	if (!isset( $_POST[$fieldsArray[1][$i]])) {
		$_POST[$fieldsArray[1][$i]] = '';
	}
	$fields = str_replace($fieldsArray[0][$i], $_POST[$fieldsArray[1][$i]], $fields);
}

if(!mail( $mailto, $subject, $fields)) {
	reportError("Mail couldn't be sent");
}

header('Location: ' . $redirect);
exit;

function reportError($x){
	if (is_string($x)) {
		trigger_error('Space MAILFORM - ' . $x, E_USER_ERROR);
	}
}
?>
