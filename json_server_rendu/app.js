import About from "./js/views/pages/About.js";
import Article from "./js/views/pages/Article.js";
import ArticleAll from "./js/views/pages/ArticleAll.js";
import ErrorPage from "./js/views/pages/ErrorPage.js";

import Utils from "./js/services/Utils.js";

const routes = {
    "/"            : About,
    "/about"       : About,
    "/articles"    : ArticleAll,
    "/article/:id" : Article,
}

const router = async () => {
    const content   = document.querySelector("#content");
    let   request   = Utils.parseRequestURL();
    console.log("router request :",request);
    let   parsedurl = `/${request.resource || ""}${request.id ? "" : "/0"}${request.verb ? `/${request.verb}` : ""}`;
    console.log("router parsedURL :",parsedurl);
    let   page      = routes[parsedurl] ? (new routes[parsedurl]()) : (new ErrorPage());
    console.log("PAGE : ",page);
    console.log("TYPEOF PAGE : ",typeof page);
    content.innerHTML = await page.render();
};

window.addEventListener("load",router);
window.addEventListener("hashchange",router);