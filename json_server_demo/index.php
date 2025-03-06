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
    <script type="module" src="./app.js" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
</head>

<body>
    <header>
        <h1>mon header todo plus tard</h1>
        <nav><ul>
            <li><a href="#/Articles">articles</a></li>
            <li><a href="#/About">about</a></li>
        </ul></nav>
    </header>
    <main>
        <div id="content">
        </div>
    </main>
    <footer>
        <p>footer HERE</p>
    </footer>
</body>

</html>