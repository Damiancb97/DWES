<?php
$host = '172.16.0.2'; // Dirección del servidor Django
$username = 'root';
$password = '1234';
$dbname = 'mysitedb';
?>
<html>
<head>
    <meta charset="UTF-8">
    <title>Lista de Juegos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        h1 a {
            float: right;
            font-size: 15px;
        }
        .container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
        }
        .item {
            background-color: #fff;
            width: 300px;
            margin: 15px;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .item img {
            max-width: 100%;
            height: auto;
            max-height: 200px; /* Tamaño fijo de la imagen */
            border-radius: 5px;
        }
        .item a {
            text-decoration: none;
            color: #007BFF;
            font-weight: bold;
        }
        .item a:hover {
            color: #0056b3;
        }
    </style>
</head>
<body>
<h1>Conexión establecida <a href="/logout.php">Logout</a></h1>
<div class="container">
<?php
// Conexión a la base de datos
$conn = new mysqli($host, $username, $password, $dbname);

// Verifica si hay errores en la conexión
if ($conn->connect_error) {
    die("Error al conectar a la base de datos: " . $conn->connect_error);
}

// Ejecuta la consulta
$query = 'SELECT * FROM tJuegos';
$result = $conn->query($query);

// Verifica si la consulta es válida
if (!$result) {
    die("Error en la consulta: " . $conn->error);
}

// Recorre el resultado
while ($row = $result->fetch_assoc()) {
    echo '<div class="item">';
    echo '<h2>' . htmlspecialchars($row['nombre']) . '</h2>';
    echo '<p><strong>Género:</strong> ' . htmlspecialchars($row['genero']) . '</p>';
    echo '<p><strong>Plataforma:</strong> ' . htmlspecialchars($row['plataforma']) . '</p>';
    echo '<p><strong>Año de lanzamiento:</strong> ' . htmlspecialchars($row['fecha_lanzamiento']) . '</p>';
    echo '<img src="' . htmlspecialchars($row['url_imagen']) . '">';
    echo '<p><a href="detail.php?id=' . htmlspecialchars($row['id']) . '">Ver más detalles</a></p>';
    echo '</div>';
}

// Cierra la conexión
$conn->close();
?>
</div>
</body>
</html>
