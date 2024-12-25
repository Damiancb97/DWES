<?php
require('fpdf.php');

// Comprobamos que los parámetros name y surname están definidos
if (!isset($_GET['name']) || !isset($_GET['surname'])) {
    die('Error: los parametros name y surname son obligatorios');
}

$name = $_GET['name'];
$surname = $_GET['surname'];
$date = date('d/m/Y'); // Fecha actual del servidor

// Clase extendida de FPDF para añadir funcionalidad
class PDF extends FPDF
{
    // Cabecera personalizada
    function Header()
    {
        // Logo principal
        $this->Image('/home/damian/DWES/opcional_pdf/logo1.png', 10, 6, 30); // (ruta, x, y, ancho)
        $this->Image('/home/damian/DWES/opcional_pdf/logo2.png', 170, 6, 30); // Segundo logo en el otro lado
        $this->SetFont('Arial', 'B', 16);
        $this->Cell(0, 10, 'Instituto de Desarrollo Web', 0, 1, 'C'); // Título centrado
        $this->Ln(10); // Espaciado
    }

    // Pie de página personalizado
    function Footer()
    {
        $this->SetY(-15); // Posición a 1.5 cm del final de la página
        $this->SetFont('Arial', 'I', 8);
        $this->Cell(0, 10, 'Pagina ' . $this->PageNo(), 0, 0, 'C');
    }
}

// Crear un nuevo PDF
$pdf = new PDF();
$pdf->AddPage();

// Fondo del diploma (Quería meterle background pero me doy por vencido, tampoco me
// convenze como quedaría ya que buscas algo púlido y limpio, que se entienda)
//$pdf->Image('/home/damian/DWES/opcional_pdf/background.png', 0, 0, 210, 297); // Tamaño A4

// Contenido del diploma
$pdf->SetFont('Times', 'B', 24);
$pdf->SetTextColor(0, 51, 102); // Azul oscuro
$pdf->Cell(0, 10, ('Diploma de Reconocimiento'), 0, 1, 'C');
$pdf->Ln(20);

$pdf->SetFont('Arial', '', 16);
$pdf->SetTextColor(0); 
$pdf->MultiCell(0, 10, ("El Instituto de Desarrollo Web otorga el presente diploma a:"), 0, 'C');
$pdf->Ln(10);

$pdf->SetFont('Courier', 'B', 20);
$pdf->SetTextColor(0, 102, 204); 
$pdf->Cell(0, 10, utf8_decode("$name $surname"), 0, 1, 'C'); //Activando el utf8_decode, te permite meter caracteres especiales.
$pdf->Ln(15);

$pdf->SetFont('Arial', '', 14);
$pdf->SetTextColor(0); 
$pdf->MultiCell(0, 10, ("Por haber demostrado habilidades excepcionales en el curso de Desarrollo Web en Entorno Servidor."), 0, 'C');
$pdf->Ln(10);

$pdf->SetFont('Arial', 'I', 12);
$pdf->SetTextColor(50, 50, 50); 
$pdf->Cell(0, 10, ("Fecha del diploma: $date"), 0, 1, 'C');

// Firma
$pdf->Ln(20);
$pdf->SetFont('Arial', '', 12);
$pdf->SetTextColor(0);
$pdf->Cell(0, 10, '_________________________', 0, 1, 'C');
$pdf->Cell(0, 10, ('Director del Instituto'), 0, 1, 'C');

// Generar y mostrar el PDF
$pdf->Output();
?>
