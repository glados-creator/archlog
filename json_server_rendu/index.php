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

  <!-- BOOTSTRAP bump version from 4.4.1 to 5.2.3 -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.2.3/js/bootstrap.min.js"
    integrity="sha512-1/RvZTcCDEUjY/CypiMz+iqqtaoQfAITmNSJY17Myp4Ms5mdxPS5UV7iOfdZoxcGhzFbOm6sntTKJppjvuhg4g=="
    crossorigin="anonymous" referrerpolicy="no-referrer"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
    integrity="sha384-sA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65'." crossorigin="anonymous"
    referrerpolicy="no-referrer">

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