import About from "./js/views/pages/About.js";
import Article from "./js/views/pages/Article.js"
import ArticleAll from "./js/views/pages/ArticleAll.js";

import Utils from "./js/services/Utils.js";

const routes = {
    "/"            : About,
    "/about"       : About,
    "/articles"    : ArticleAll,
    "/articles/:id": Article,
}

const router = async () => {
    const content   = document.querySelector("#content");
    let   request   = Utils.parseRequestURL();
    console.log("router request :",request);
    let   parsedurl = "/"+(request.resource ? request.resource : "") + (request.id ? "/:id" : "") + (request.verb ? "/"+request.verb : "");
    console.log("router parsedURL :",parsedurl);
    let   page      = routes[parsedurl] ? (new routes[parsedurl]()) : (new About());
    console.log(page);
    console.log(typeof page);
    console.log(typeof page.render);
    content.innerHTML = await page.render();
};

window.addEventListener("load",router);
window.addEventListener("hashchange",router);