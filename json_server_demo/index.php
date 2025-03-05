<?php
header('Access-Control-Allow-Origin: *');

header('Access-Control-Allow-Methods: GET, POST');

header("Access-Control-Allow-Headers: X-Requested-With");
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>json_server_demo</title>
</head>
<body>
    <header>
        <h1>mon header todo plus tard</h1>
    </header>
    <main>
        <div id="content">
        </div>
    </main>
    <footer>
        <p>footer HERE</p>
    </footer>

    <script type="module" src="app.js">
    </script>
</body>
</html>