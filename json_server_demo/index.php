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
    <link rel="stylesheet" href="https://bootswatch.com/5/darkly/bootstrap.min.css">   
    <script type="module" src="./app.js" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
</head>

<body>

<div class="bs-component">
              <nav class="navbar navbar-expand-lg bg-primary" data-bs-theme="dark">
                <div class="container-fluid">
                  <a class="navbar-brand" href="#/">LAW AND ORDER</a>
                  <div class="collapse navbar-collapse" id="navbarColor01">
                    <ul class="navbar-nav me-auto">
                      <li class="nav-item">
                        <a class="nav-link" href="#/articles">Articles</a>
                      </li>
                      <li class="nav-item">
                        <a class="nav-link" href="#/about">About</a>
                      </li>
                    </ul>
                  </div>
                </div>
              </nav>
        </div>
            
    <main>
        <div id="content">
        </div>
    </main>
    <footer>
        <p>footer HERE</p>
    </footer>
</body>

</html>