import ProviderArticle from "../../services/ProviderArticle.js";
export default class ArticleAll {
    async render(){
        let article = await ProviderArticle.FetchArticles({page : 10,limite : 50});
        let view = `
            <h2>les articles</h2>
            <ul>
            ${article.map(
                article => {
                    return `<li><a href=article?=${article.id}>${article.title}</li>`;
                }
            ).join("\n")}
            </ul>`;
            return view;
    }
}