$(function() {
    const apiBaseUrl = 'proxy.php?url=http://127.0.0.1:5000/api/v1.0.0';

    $("#add-article").click(formArticle);
    $("#del-article").click(delArticle);
    $("#refresh-articles").click(refreshArticleList);
    $("#add-comment").click(() => formComment(true));

    function refreshArticleList() {
        $("#currenttask").empty();
        fetch(`${apiBaseUrl}/articles`)
            .then(response => {
                if (response.ok) return response.json();
                else throw new Error('Error fetching articles: ' + response.status);
            })
            .then(fetchArticleDetails)
            .catch(onError);
    }

    function fetchArticleDetails(articleIds) {
        const articlePromises = articleIds.map(articleId =>
            fetch(`${apiBaseUrl}/articles/${articleId.id}`)
                .then(response => {
                    if (response.ok) return response.json();
                    else throw new Error('Error fetching article details: ' + response.status);
                })
        );

        Promise.all(articlePromises)
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
        const article = event.data;
        $("#currenttask").empty();
        $("#currenttask").append(`
            <h3>${article.title}</h3>
            <p>${article.content}</p>
        `);
        formArticle(false, article);
        fetchComments(article.id);
    }

    function formArticle(isNew = true, article = null) {
        $("#currenttask").append('<hr>');
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
            .then(commentIds => {
                const commentPromises = commentIds.map(commentId =>
                    fetch(`${apiBaseUrl}/comment/${commentId.id}`)
                        .then(response => {
                            if (response.ok) return response.json();
                            else throw new Error('Error fetching comment details: ' + response.status);
                        })
                );
                return Promise.all(commentPromises);
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
                    .append($('<button class="btn btn-sm btn-danger ml-2">Delete</button>')
                        .on("click", function() { delComment(comment.id); }))
                    .append($('<button class="btn btn-sm btn-primary ml-2">Edit</button>')
                        .on("click", function() { formComment(false, comment); }))
                );
        });
        $('#comments').append($('<button class="btn btn-sm btn-secondary mt-2">Add Comment</button>')
            .on("click", () => formComment(true)));
    }

    function formComment(isNew = true, comment = null) {
        $("#currenttask").empty();
        $("#currenttask")
            .append($('<span>Content<textarea id="comment-content"></textarea><br></span>'))
            .append($('<span><input type="hidden" id="comment-id"><br></span>'))
            .append(isNew ?
                $('<span><input type="button" value="Save Comment"><br></span>').on("click", saveNewComment) :
                $('<span><input type="button" value="Modify Comment"><br></span>').on("click", saveModifiedComment)
            );

        if (!isNew && comment) {
            $("#comment-content").val(comment.content);
            $("#comment-id").val(comment.id);
        }
    }

    function saveNewComment() {
        const comment = {
            content: $("#comment-content").val(),
            article_id: $("#article-id").val()
        };

        fetch(`${apiBaseUrl}/comments/${comment.article_id}`, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(comment)
        })
        .then(response => {
            if (response.ok) {
                console.log('Save Comment Success');
                fetchComments(comment.article_id);
            } else {
                throw new Error('Error saving comment');
            }
        })
        .catch(onError);
    }

    function saveModifiedComment() {
        const comment = {
            id: $("#comment-id").val(),
            content: $("#comment-content").val()
        };

        fetch(`${apiBaseUrl}/comment/${comment.id}`, {
            method: "PUT",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(comment)
        })
        .then(response => {
            if (response.ok) {
                console.log('Update Comment Success');
                fetchComments($("#article-id").val());
            } else {
                throw new Error('Error updating comment');
            }
        })
        .catch(onError);
    }

    function delComment(commentId) {
        fetch(`${apiBaseUrl}/comment/${commentId}`, {
            method: "DELETE",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                console.log('Delete Comment Success');
                fetchComments($("#article-id").val());
            } else {
                throw new Error('Error deleting comment');
            }
        })
        .catch(onError);
    }

    function onError(err) {
        $("#currenttask").html("<b>Error: </b>" + err);
    }

    // Initialize
    refreshArticleList();
});
