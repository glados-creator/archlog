<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, DELETE, PUT, OPTIONS');
header("Access-Control-Allow-Headers: X-Requested-With, Content-Type");
header("Referrer-Policy: unsafe-url");

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Define allowed domains (optional for security)
$allowed_domains = [
    "localhost",
    "127.0.0.1"
];

// Get target URL
$target = $_GET['url'] ?? null;
if (!$target || !filter_var($target, FILTER_VALIDATE_URL)) {
    http_response_code(400);
    echo json_encode(["error" => "Invalid URL"]);
    exit;
}

// Check domain security
$parsed_url = parse_url($target);
if (!in_array($parsed_url['host'], $allowed_domains)) {
    http_response_code(403);
    echo json_encode(["error" => "Domain not allowed"]);
    exit;
}

// Initialize cURL
$ch = curl_init($target);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); // Ignore SSL issues

// Set request method
$method = $_SERVER['REQUEST_METHOD'];
if ($method === 'POST') {
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, file_get_contents("php://input"));
} elseif ($method === 'DELETE') {
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'DELETE');
} elseif ($method === 'PUT') {
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PUT');
    curl_setopt($ch, CURLOPT_POSTFIELDS, file_get_contents("php://input"));
}

// Set headers
$headers = getallheaders();
$curl_headers = [];
foreach ($headers as $key => $value) {
    if (!in_array(strtolower($key), ['host', 'content-length'])) {
        $curl_headers[] = "$key: $value";
    }
}
curl_setopt($ch, CURLOPT_HTTPHEADER, $curl_headers);

// Execute request
$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

// Return response
http_response_code($http_code);
echo $response;
?>
