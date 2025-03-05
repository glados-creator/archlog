import ProviderArticle from "../../services/ProviderArticle.js";
export default class ArticleAll {
    static async render(){
        let article = await ProviderArticle.FetchArticles(20);
        let view = `
            <h2>les articles</h2>
            <ul>
            ${article.map(
                article => {
                    return `<li>${article.title}</li>`;
                }
            ).join("\n")}
            </ul>`;
            return view;
    }
}