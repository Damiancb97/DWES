<?php
require('fpdf.php');

$pdf = new FPDF();
$pdf->AddPage();
$pdf->Image('/home/damian/DWES/opcional_pdf/background.png', 10, 10, 50);// Ruta absoluta
$pdf->Output();
?>
