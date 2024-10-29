<?php
	$db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Fail');
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
<h1>Conexión establecida</h1>
	<?php
	// Lanzar una query
	$query = 'SELECT * FROM tJuegos';
	$result = mysqli_query($db, $query) or die('Query error');
	// Recorrer el resultado
	while ($row = mysqli_fetch_array($result)){
        echo '<div class="item">';
        // Mostrar el nombre del juego
        echo '<h2>' . htmlspecialchars($row['nombre']) . '</h2>';
        
        // Mostrar más detalles (género, plataforma, etc.)
        echo '<p><strong>Género:</strong> ' . htmlspecialchars($row['genero']) . '</p>';
        echo '<p><strong>Plataforma:</strong> ' . htmlspecialchars($row['plataforma']) . '</p>';
        echo '<p><strong>Año de lanzamiento:</strong> ' . htmlspecialchars($row['fecha_lanzamiento']) . '</p>';
        
        // Mostrar la imagen del juego
        echo '<img src="'. htmlspecialchars($row['url_imagen']) . '">';        
        // Enlace a detail.php con el ID del juego
        echo '<p><a href="detail.php?id=' . htmlspecialchars($row['id']) . '">Ver más detalles</a></p>';
        echo '</div>';
    }

	// Cerrar la conexión
	mysqli_close($db); 
	?>
</body>
</html>