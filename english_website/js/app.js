$(document).ready(function () {
    // Theme Toggle
    $("#theme-toggle").click(function () {
        $("body").toggleClass("dark-mode");
        let mode = $("body").hasClass("dark-mode") ? "dark" : "light";
        localStorage.setItem("theme", mode);
        $("#theme-toggle").text(mode === "dark" ? "☀️" : "🌙");
    });

    // Remember theme setting
    if (localStorage.getItem("theme") === "dark") {
        $("body").addClass("dark-mode");
        $("#theme-toggle").text("☀️");
    }
});
