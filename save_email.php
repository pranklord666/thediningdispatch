<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = filter_input(INPUT_POST, 'email', FILTER_VALIDATE_EMAIL);

    if ($email) {
        $file = 'emails.txt';
        file_put_contents($file, $email . PHP_EOL, FILE_APPEND | LOCK_EX);
        echo 'Vous êtes inscrit à la newsletter!';
    } else {
        echo 'Email invalide.';
    }
} else {
    echo 'Méthode non autorisée.';
}
?>
