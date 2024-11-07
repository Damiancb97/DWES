<?php
    $db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Fail');
    
    $email_posted = $_POST['f_email'];
    $password_posted = $_POST['f_password'];

    // Consulta preparada para evitar inyección SQL
    $query = "SELECT id, contraseña FROM tUsuarios WHERE email = ?";
    $stmt = mysqli_prepare($db, $query);
    mysqli_stmt_bind_param($stmt, 's', $email_posted);
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);

    $query = "SELECT id, contraseña FROM tUsuarios WHERE email = '".$email_posted."'";
    $result = mysqli_query($db, $query) or die('Query error'); 
if (mysqli_num_rows($result) > 0) {
    $only_row = mysqli_fetch_array($result);
    if (password_verify($password_posted, $only_row['contraseña'])) {
        session_start();
        $_SESSION['user_id'] = $only_row[0];
        header('Location: main.php');
    } else {
        echo '<p>Contraseña incorrecta</p>';
    }
    } else {
        echo '<p>Usuario no encontrado con ese email</p>';
    }
?>