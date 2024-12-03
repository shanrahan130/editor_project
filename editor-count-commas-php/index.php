<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

if (isset($_GET['text'])) {
    $text = $_GET['text'];
    $count = substr_count($text, ",");
    $response = array(
        "error" => false,
        "string" => "Contains " . $count . " commas",
        "answer" => $count
    );
} else {
    $response = array(
        "error" => true,
        "string" => "No text provided",
        "answer" => 0
    );
}

echo json_encode($response);
?>
