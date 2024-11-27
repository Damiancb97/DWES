<?php
$host = '172.16.0.2'; // Dirección del servidor Django
$username = 'root';
$password = '1234';
$dbname = 'mysitedb';

// Conexión a la base de datos
$conn = new mysqli($host, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Error al conectar a la base de datos: " . $conn->connect_error);
}

// Validar si los datos del formulario están presentes
if (!isset($_POST['f_email']) || !isset($_POST['f_password'])) {
    die('Error: Datos no válidos.');
}

$email_posted = trim($_POST['f_email']);
$password_posted = trim($_POST['f_password']);

// Consulta preparada para buscar al usuario por email
$query = "SELECT id, contraseña FROM tUsuarios WHERE email = ?";
$stmt = $conn->prepare($query);
$stmt->bind_param('s', $email_posted);
$stmt->execute();
$result = $stmt->get_result();

// Verificar si el usuario existe
if ($result->num_rows > 0) {
    $only_row = $result->fetch_assoc();
    // Verificar la contraseña
    if (password_verify($password_posted, $only_row['contraseña'])) {
        session_start();
        $_SESSION['user_id'] = $only_row['id'];
        header('Location: main.php');
        exit;
    } else {
        echo '<p>Credenciales incorrectas</p>';
    }
} else {
    echo '<p>Credenciales incorrectas</p>';
}

// Cerrar la conexión
$stmt->close();
$conn->close();
?>
