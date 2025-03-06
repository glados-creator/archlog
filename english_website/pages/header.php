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
    <title>Neptune Next</title>
    
        <!-- JQUERRY bump version from 3.4.1 to 3.7.1 -->
        <script src="https://code.jquery.com/jquery-3.7.1.min.js"
        integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo=" crossorigin="anonymous"
        referrerpolicy="no-referrer"></script>
    <!-- JQUERRY-UI bump from 1.12.1 to 1.14 -->
    <script src="https://code.jquery.com/ui/1.14.1/jquery-ui.min.js"
        integrity="sha256-AlTido85uXPlSyyaZNsjJXeCs07eSv3r43kyCVc8ChI=" crossorigin="anonymous"
        referrerpolicy="no-referrer"></script>
    <link rel="stylesheet" href="https://code.jquery.com/ui/1.14.1/themes/base/jquery-ui.css"
        integrity="sha256-LUpAU8h+pO1VS/mXF6vWuo3QKtT9m/SUElNjr1CX8='." crossorigin="anonymous"
        referrerpolicy="no-referrer">
    <!-- POPPER.JS i have no idears -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.1/umd/popper.min.js"
        integrity="sha512-ubuT8Z88WxezgSqf3RLuNi5lmjstiJcyezx34yIU2gAHonIi27Na7atqzUZCOoY4CExaoFumzOsFQ2Ch+I/HCw=="
        crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <!-- BOOTSTRAP bump version from 4.4.1 to 5.2.3 -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.2.3/js/bootstrap.min.js"
        integrity="sha512-1/RvZTcCDEUjY/CypiMz+iqqtaoQfAITmNSJY17Myp4Ms5mdxPS5UV7iOfdZoxcGhzFbOm6sntTKJppjvuhg4g=="
        crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
        integrity="sha384-sA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65'." crossorigin="anonymous"
        referrerpolicy="no-referrer">

    <!-- LOCALS -->
    <link rel="stylesheet" href="../css/style.css" />
    <script src="../js/app.js"></script>
</head>
<body>
<header class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
        <a class="navbar-brand" href="index.php">Neptune Next</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item"><a class="nav-link" href="home.php">Home</a></li>
                <li class="nav-item"><a class="nav-link" href="about.php">About</a></li>
                <li class="nav-item"><a class="nav-link" href="map.php">Map</a></li>
            </ul>
        </div>
        <button id="theme-toggle" class="btn btn-light">🌙</button>
    </div>
</header>