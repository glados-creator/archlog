import { ENDPOINT } from "../config.js";
export default class ProviderArticle {

    static FetchArticles = async (limite=10) => {
        const options = {
            methode : "GET",
            header : {
                "Content-Type" : "application/json"
            }
        };

        try {
            const rep = await fetch(`${ENDPOINT}?_limit=${limite}`,options);
            const json = await rep.json();
            return json;
        } catch (error) {
            console.error(error);
            return {};
        }
    }

    static GetArticles = async (id) => {
        const options = {
            methode : "GET",
            header : {
                "Content-Type" : "application/json"
            }
        };

        try {
            const rep = await fetch(`${ENDPOINT}/${id}`,options);
            const json = await rep.json();
            return json;
        } catch (error) {
            console.error(error);
            return {};
        }
    }

}