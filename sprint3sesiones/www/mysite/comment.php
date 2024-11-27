<?php
$host = '172.16.0.2'; // Dirección del servidor Django
$username = 'root';
$password = '1234';
$dbname = 'mysitedb';
?>
<html>
    <body>
        <?php
        session_start();

        // Establecer conexión a la base de datos
        $conn = new mysqli($host, $username, $password, $dbname);
        if ($conn->connect_error) {
            die("Error al conectar a la base de datos: " . $conn->connect_error);
        }

        // Validar y obtener datos del formulario
        if (!isset($_POST['juego_id']) || !isset($_POST['new_comment'])) {
            die('Datos no válidos.');
        }

        $juego_id = intval($_POST['juego_id']); // Asegura que es un número entero
        $comentario = trim($_POST['new_comment']); // Elimina espacios en blanco

        if (empty($comentario)) {
            die('El comentario no puede estar vacío.');
        }

        // Obtener el ID del usuario si está en la sesión
        $user_id_a_insertar = null;
        if (!empty($_SESSION['user_id'])) {
            $user_id_a_insertar = intval($_SESSION['user_id']);
        }

        // Inserción segura del comentario
        $stmt = $conn->prepare('INSERT INTO tComentarios (comentario, juego_id, usuario_id) VALUES (?, ?, ?)');
        $stmt->bind_param('sii', $comentario, $juego_id, $user_id_a_insertar);
        if ($stmt->execute()) {
            echo "<p>Nuevo comentario con ID ";
            echo $stmt->insert_id; // Obtiene el ID del nuevo comentario
            echo " añadido</p>";
        } else {
            echo "<p>Error al añadir el comentario.</p>";
        }
        $stmt->close();

        echo "<a href='/detail.php?id=" . htmlspecialchars($juego_id) . "'>Volver</a>";

        // Cerrar la conexión
        $conn->close();
        ?>
    </body>
</html>

