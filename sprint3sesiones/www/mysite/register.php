<?php
    $db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Fail');
    
    // Obtener datos del formulario
    $email_posted = trim($_POST['f_email']);
    $password_posted = $_POST['f_password'];
    $confirm_password_posted = $_POST['f_confirm_password'];

    // Verificar que no haya campos vacíos
    if (empty($email_posted) || empty($password_posted) || empty($confirm_password_posted)) {
        echo '<p>Todos los campos son obligatorios</p>';
        exit;
    }

    // Verificar que las contraseñas coincidan
    if ($password_posted !== $confirm_password_posted) {
        echo '<p>Las contraseñas no coinciden</p>';
        exit;
    }

    $query = "SELECT id FROM tUsuarios WHERE email = ?";
    $stmt = mysqli_prepare($db, $query);
    mysqli_stmt_bind_param($stmt, 's', $email_posted);
    mysqli_stmt_execute($stmt);
    mysqli_stmt_store_result($stmt);

    if (mysqli_stmt_num_rows($stmt) > 0) {
        echo '<p>El correo ya está registrado</p>';
        exit;
    }
        
    // Cifrar la contraseña antes de guardarla
    $hashed_password = password_hash($password_posted, PASSWORD_DEFAULT);

    // Insertar el nuevo usuario en la base de datos
    $query = "INSERT INTO tUsuarios (email, contraseña) VALUES (?, ?)";
    $stmt = mysqli_prepare($db, $query);
    mysqli_stmt_bind_param($stmt, 'ss', $email_posted, $hashed_password);

    if (mysqli_stmt_execute($stmt)) {
        // Iniciar sesión automáticamente después del registro
        session_start();
        $_SESSION['user_id'] = mysqli_insert_id($db);
        
        // Redirigir al usuario a la página principal
        header('Location: main.php');
        exit;
    } else {
        echo '<p>Error al registrar el usuario</p>';
    }
?>