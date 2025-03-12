import Utils  from "../../services/Utils.js";
import ProviderArticle from "../../services/ProviderArticle.js";
export default class Article {
    async render() {
        let url = document.querySelector("#content");
        let request = Utils.parseRequestURL(url);
        let art = await ProviderArticle.GetArticles(request.id);
        console.log("ARTICLE : ",art);
        return `
        <h2>titre : ${art.title}</h2>
        <h4>text :</h4><p>${art.text}</p>
        <h4>modified_by :</h4><p>${art.modified_by}</p>
        <h4>see more :</h4><p>${art.see_more}</p>
        `;
    }
}