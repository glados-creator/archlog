$(function() {
    const apiBaseUrl = '/api/v1.0.0';

    $("#add-article").click(formArticle);
    $("#del-article").click(delArticle);

    function refreshArticleList() {
        $("#currenttask").empty();
        fetch(`${apiBaseUrl}/articles`)
            .then(response => {
                if (response.ok) return response.json();
                else throw new Error('Error fetching articles: ' + response.status);
            })
            .then(fillArticles)
            .catch(onError);
    }

    function fillArticles(articles) {
        $('#articles').empty();
        $('#articles').append($('<ul>'));
        articles.forEach(article => {
            $('#articles ul')
                .append($('<li>')
                    .append($('<a>')
                        .text(article.title)
                    ).on("click", article, showArticleDetails)
                );
        });
    }

    function showArticleDetails(event) {
        $("#currenttask").empty();
        formArticle(false, event.data);
        fetchComments(event.data.id);
    }

    function formArticle(isNew = true, article = null) {
        $("#currenttask").empty();
        $("#currenttask")
            .append($('<span>Title<input type="text" id="article-title"><br></span>'))
            .append($('<span>Content<textarea id="article-content"></textarea><br></span>'))
            .append($('<span><input type="hidden" id="article-id"><br></span>'))
            .append(isNew ?
                $('<span><input type="button" value="Save Article"><br></span>').on("click", saveNewArticle) :
                $('<span><input type="button" value="Modify Article"><br></span>').on("click", saveModifiedArticle)
            );

        if (!isNew && article) {
            $("#article-title").val(article.title);
            $("#article-content").val(article.content);
            $("#article-id").val(article.id);
        }
    }

    function saveNewArticle() {
        const article = {
            title: $("#article-title").val(),
            content: $("#article-content").val()
        };

        fetch(`${apiBaseUrl}/articles`, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(article)
        })
        .then(response => {
            if (response.ok) {
                console.log('Save Success');
                refreshArticleList();
            } else {
                throw new Error('Error saving article');
            }
        })
        .catch(onError);
    }

    function saveModifiedArticle() {
        const article = {
            id: $("#article-id").val(),
            title: $("#article-title").val(),
            content: $("#article-content").val()
        };

        fetch(`${apiBaseUrl}/articles/${article.id}`, {
            method: "PUT",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(article)
        })
        .then(response => {
            if (response.ok) {
                console.log('Update Success');
                refreshArticleList();
            } else {
                throw new Error('Error updating article');
            }
        })
        .catch(onError);
    }

    function delArticle() {
        const articleId = $("#article-id").val();
        if (articleId) {
            fetch(`${apiBaseUrl}/articles/${articleId}`, {
                method: "DELETE",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.ok) {
                    console.log('Delete Success');
                    refreshArticleList();
                } else {
                    throw new Error('Error deleting article');
                }
            })
            .catch(onError);
        }
    }

    function fetchComments(articleId) {
        fetch(`${apiBaseUrl}/article/${articleId}/comments`)
            .then(response => {
                if (response.ok) return response.json();
                else throw new Error('Error fetching comments: ' + response.status);
            })
            .then(fillComments)
            .catch(onError);
    }

    function fillComments(comments) {
        $('#comments').empty();
        $('#comments').append($('<ul>'));
        comments.forEach(comment => {
            $('#comments ul')
                .append($('<li>')
                    .text(comment.content)
                );
        });
    }

    function onError(err) {
        $("#currenttask").html("<b>Error: </b>" + err);
    }

    // Initialize
    refreshArticleList();
});
