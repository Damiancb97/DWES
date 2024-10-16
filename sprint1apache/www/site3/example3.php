<html>
<body>
<h1>Jubilación</h1>
<?php
function edad_en_10_años($edad) {
return $edad + 10;
}
$v_edad= $_GET["edad"];
if (edad_en_10_años($v_edad) > 65) {
echo "En 10 años tendrás edad de jubilación";
} else {
echo "¡Disfruta de tu tiempo!";
}
?>
</body>
</html>
