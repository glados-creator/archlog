$(function() {

    fetch("http://127.0.0.1:5000/quizz/api/v1.0/login").then(console.log).catch(console.log);

    $("#Qbutton").click(refreshQuestionnaire);
    $("#question-panel").click(refreshQuestion);
    $("#response-panel").click(refreshResponse);

    function fillListQuestionnaire(repjson) {
        console.log(JSON.stringify(repjson));
        $('#Qquestionnaires').empty();
        $('#Qquestionnaires').append($('<ul>'));
        for (let quiz of repjson.quizzes) {
            $('#Qquestionnaires ul')
                .append($('<li>')
                    .append($('<a>')
                        .text(quiz.title)
                    ).on("click", quiz, editQuiz)
                );
        }
    }

    function refreshQuestionnaire() {
        $("#Qquestionnaires").empty();
        fetch("http://127.0.0.1:5000/quizz/api/v1.0/questionnaire")
            .then(response => {
                if (response.ok) return response.json();
                else throw new Error('AJAX Error: ' + response.status);
            })
            .then(fillListQuestionnaire)
            .catch((err) => {
                console.trace(err);
                $("#Qquestionnaires").html("<b>Impossible de récupérer les Questionnaires</b>" + err);
            });
    }

    function fillListQuestion(repjson) {
        console.log(JSON.stringify(repjson));
        $('#question-list').empty();
        $('#question-list').append($('<ul>'));
        for (let question of repjson.questions) {
            $('#question-list ul')
                .append($('<li>')
                    .append($('<a>')
                        .text(question.text)
                    ).on("click", question, editQuestion)
                );
        }
    }

    function refreshQuestion() {
        $("#current-question").empty();
        fetch("http://127.0.0.1:5000/quizz/api/v1.0/questions")
            .then(response => {
                if (response.ok) return response.json();
                else throw new Error('AJAX Error: ' + response.status);
            })
            .then(fillListQuestion)
            .catch((err) => {
                console.trace(err);
                $("#Qquestionnaires").html("<b>Impossible de récupérer les Questionnaires</b>" + err);
            });
    }

    // Response functions
    function fillResponseList(repjson) {
        console.log(JSON.stringify(repjson));
        $('#response-list').empty();
        $('#response-list').append($('<ul>'));
        for (let response of repjson.responses) {
            $('#response-list ul')
                .append($('<li>')
                    .append($('<a>')
                        .text(response.text)
                    ).on("click", response, editResponse)
                );
        }
    }

    function refreshResponse() {
        $("#current-response").empty();
        fetch("http://127.0.0.1:5000/quizz/api/v1.0/responses")
            .then(response => {
                if (response.ok) return response.json();
                else throw new Error('AJAX Error: ' + response.status);
            })
            .then(fillResponseList)
            .catch(onError);
    }

    // Edit Quiz, Question, and Response
    function editQuiz(event) {
        $("#current-quiz").empty();
        formQuiz();
        fillFormQuiz(event.data);
    }

    function editQuestion(event) {
        $("#current-question").empty();
        formQuestion();
        fillFormQuestion(event.data);
    }

    function editResponse(event) {
        $("#current-response").empty();
        formResponse();
        fillFormResponse(event.data);
    }

    // CRUD operations for Quiz
    function formQuiz(isNew) {
        $("#current-quiz").empty();
        $("#current-quiz")
            .append($('<span>Title<input type="text" id="quiz-title"><br></span>'))
            .append($('<span>Description<input type="text" id="quiz-desc"><br></span>'))
            .append(isNew ? $('<span><input type="button" value="Save Quiz"><br></span>').on("click", saveNewQuiz)
                          : $('<span><input type="button" value="Modify Quiz"><br></span>').on("click", saveModifiedQuiz));
    }

    function fillFormQuiz(quiz) {
        $("#current-quiz #quiz-title").val(quiz.title);
        $("#current-quiz #quiz-desc").val(quiz.description);
        $("#current-quiz #quiz-uri").val(quiz.uri);
    }

    function saveNewQuiz() {
        var quiz = new Questionnaire(
            $("#current-quiz #quiz-title").val(),
            $("#current-quiz #quiz-desc").val()
        );
        console.log(JSON.stringify(quiz));
        fetch("http://127.0.0.1:5000/quizz/api/v1.0/quizzes", {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify(quiz)
        })
        .then(res => {
            console.log('Save Success');
            refreshQuizzes();
        })
        .catch(res => {
            console.log(res);
        });
    }

    function saveModifiedQuiz() {
        var quiz = new Questionnaire(
            $("#current-quiz #quiz-title").val(),
            $("#current-quiz #quiz-desc").val(),
            $("#current-quiz #quiz-uri").val()
        );
        console.log("PUT");
        fetch(quiz.uri, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "PUT",
            body: JSON.stringify(quiz)
        })
        .then(res => {
            console.log('Update Success');
            refreshQuizzes();
        })
        .catch(res => {
            console.log(res);
        });
    }

    function delQuiz() {
        if ($("#current-quiz #quiz-uri").val()) {
            const url = $("#current-quiz #quiz-uri").val();
            fetch(url, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                method: "DELETE"
            })
            .then(res => {
                console.log('Delete Success');
                refreshQuizzes();
            })
            .catch(res => {
                console.log(res);
            });
        }
    }

    // CRUD operations for Question
    function formQuestion(isNew) {
        $("#current-question").empty();
        $("#current-question")
            .append($('<span>Text<input type="text" id="question-text"><br></span>'))
            .append($('<span><input type="button" value="Save Question"><br></span>').on("click", saveNewQuestion));
    }

    function fillFormQuestion(question) {
        $("#current-question #question-text").val(question.text);
    }

    function saveNewQuestion() {
        var question = new Question(
            $("#current-question #question-text").val()
        );
        console.log(JSON.stringify(question));
        fetch("http://127.0.0.1:5000/quizz/api/v1.0/questions", {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify(question)
        })
        .then(res => {
            console.log('Save Success');
            refreshQuestions();
        })
        .catch(res => {
            console.log(res);
        });
    }

    // CRUD operations for Response
    function formResponse(isNew) {
        $("#current-response").empty();
        $("#current-response")
            .append($('<span>Text<input type="text" id="response-text"><br></span>'))
            .append(isNew ? $('<span><input type="button" value="Save Response"><br></span>').on("click", saveNewResponse)
                          : $('<span><input type="button" value="Modify Response"><br></span>').on("click", saveModifiedResponse));
    }

    function fillFormResponse(response) {
        $("#current-response #response-text").val(response.text);
    }

    function saveNewResponse() {
        var response = new Response(
            $("#current-response #response-text").val()
        );
        console.log(JSON.stringify(response));
        fetch("http://127.0.0.1:5000/quizz/api/v1.0/responses", {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify(response)
        })
        .then(res => {
            console.log('Save Success');
            refreshResponses();
        })
        .catch(res => {
            console.log(res);
        });
    }

    class Questionnaire {
        constructor(id, title,questions) {
            this.id = id;
            this.title = title;
            this.questions = questions;
        }
    }

    class Question {
        constructor(id, title,reponse,user) {
            this.id = id;
            this.title = title;
            this.reponse = reponse;
            this.user = user;
        }
    }

    class Response {
        constructor(text) {
            this.text = text;
        }
    }
});
