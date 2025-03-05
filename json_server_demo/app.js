import About from "./js/views/pages/About.js";
import ArticleAll from "./js/views/pages/ArticleAll.js";

window.addEventListener("load",async () => {
    const content = document.querySelector("#content");
    content.innerHTML = await ArticleAll.render();
    content.innerHTML += await About.render();
});