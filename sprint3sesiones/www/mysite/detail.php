<?php
$host = '172.16.0.2'; // Dirección del servidor Django
$username = 'root';
$password = '1234';
$dbname = 'mysitedb';
?>
<html>
    <head>
        <style>
            .item img {
                max-width: 100%;
                height: auto;
                max-height: 200px; /* Tamaño fijo de la imagen */
                border-radius: 5px;
            }
        </style>
    </head>
<body>
<?php
// Verifica si se especificó un ID
if (!isset($_GET['id'])) {
    die('No se ha especificado un juego');
}

// Conexión a la base de datos
$conn = new mysqli($host, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Error al conectar a la base de datos: " . $conn->connect_error);
}

// Obtiene el ID del juego de forma segura
$juego_id = intval($_GET['id']);

// Consulta para obtener los detalles del juego
$stmt = $conn->prepare('SELECT * FROM tJuegos WHERE id = ?');
$stmt->bind_param('i', $juego_id);
$stmt->execute();
$result = $stmt->get_result();

// Verifica si el juego existe
if ($result->num_rows === 0) {
    die('Juego no encontrado');
}

$only_row = $result->fetch_assoc();
echo '<img src="'. htmlspecialchars($only_row['url_imagen']) . '" style="width:150px; height:100px;">';
echo '<h1>' . htmlspecialchars($only_row['nombre']) . '</h1>';
echo '<h2>' . htmlspecialchars($only_row['fecha_lanzamiento']) . '</h2>';
$stmt->close();
?>

<h3>Comentarios:</h3>
<ul>
    <?php
    // Consulta para obtener los comentarios del juego
    $stmt2 = $conn->prepare('SELECT * FROM tComentarios WHERE juego_id = ?');
    $stmt2->bind_param('i', $juego_id);
    $stmt2->execute();
    $result2 = $stmt2->get_result();

    while ($row = $result2->fetch_assoc()) {
        echo '<li>' . htmlspecialchars($row['comentario']) . '</li>';
    }
    $stmt2->close();
    ?>
</ul>

<p>Deja un nuevo comentario:</p>
<form action="/comment.php" method="post">
    <textarea rows="4" cols="50" name="new_comment"></textarea><br>
    <input type="hidden" name="juego_id" value="<?php echo htmlspecialchars($juego_id); ?>">
    <input type="submit" value="Comentar">
</form>

<?php
// Cierra la conexión a la base de datos
$conn->close();
?>
</body>
</html>
