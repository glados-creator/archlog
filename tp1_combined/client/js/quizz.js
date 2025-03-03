$(function() {
    // Improved initial login fetch
    fetch("http://127.0.0.1:5000/quizz/api/v1.0/login")
        .then(response => response.json())
        .then(data => console.log('Login response:', data))
        .catch(err => console.error('Login error:', err));

    $("#Qbutton").click(refreshQuestionnaire);
    $("#Qtool #QaddQuiz").click(() => formQuiz(true)); // Changed to create new quiz
    $("#Qtool #QaddQuestion").click(() => formQuestion(true)); // Changed to create new question

    function fillListQuestionnaire(repjson) {
        console.log(JSON.stringify(repjson));
        $('#Qquestionnaires').empty();
        $('#Qquestionnaires').append($('<ul>'));
        for (let quizData of repjson.questionnaire) {  
            const quiz = new Questionnaire(quizData.id, quizData.name, quizData.questions);
            $('#Qquestionnaires ul')
                .append($('<li>')
                    .append($('<a>')
                        .text(quiz.title)
                    ).on("click", quiz, editQuiz)
                );
        }
    }

    function refreshQuestionnaire() {
        $("#Qcurrentquestion").empty();
        fetch("http://127.0.0.1:5000/quizz/api/v1.0/questionnaire")
            .then(response => {
                if (!response.ok) throw new Error('AJAX Error: ' + response.status);
                return response.json();
            })
            .then(fillListQuestionnaire)
            .catch((err) => {
                console.trace(err);
                $("#Qquestionnaires").html("<b>Impossible de récupérer les Questionnaires</b>" + err);
            });
    }

    function fillListQuestion(repjson) {
        console.log(JSON.stringify(repjson));
        $('#Qcurrentquestion2').empty(); // Use second section for questions
        $('#Qcurrentquestion2').append($('<ul>'));
        for (let questionData of repjson) {
            const question = new Question(questionData.id, questionData.title, questionData.reponse);
            $('#Qcurrentquestion2 ul')
                .append($('<li>')
                    .append($('<a>')
                        .text(question.title)
                    ).on("click", question, editQuestion)
                );
        }
    }

    function fetchQuestionsForQuestionnaire(quizId) {
        $("#Qcurrentquestion2").empty();
        fetch(`http://127.0.0.1:5000/quizz/api/v1.0/questionnaire/${quizId}`)
            .then(response => {
                if (!response.ok) throw new Error('AJAX Error: ' + response.status);
                return response.json();
            })
            .then(fillListQuestion)
            .catch((err) => {
                console.trace(err);
                $("#Qcurrentquestion2").html("<b>Impossible de récupérer les Questions du Questionnaire</b>" + err);
            });
    }

    // Edit functions using classes
    function editQuiz(event) {
        $("#Qcurrentquestion").empty();
        formQuiz(false);
        fillFormQuiz(event.data);
        fetchQuestionsForQuestionnaire(event.data.id); // Fetch questions for selected quiz
    }

    function editQuestion(event) {
        $("#Qcurrentquestion").empty();
        formQuestion(false);
        fillFormQuestion(event.data);
        // Optionally fetch responses for this question here if needed
    }

    function editResponse(event) {
        $("#Qcurrentquestion").empty();
        formResponse(false);
        fillFormResponse(event.data);
    }

    // CRUD operations for Quiz
    function formQuiz(isNew = true) {
        $("#Qcurrentquestion").empty();
        $("#Qcurrentquestion")
            .append($('<span>Titre<input type="text" id="quiz-title"><br></span>'))
            .append($('<span><input type="hidden" id="quiz-uri"><br></span>'))
            .append(isNew ?
                $('<span><input type="button" value="Save Quiz"><br></span>').on("click", saveNewQuiz) :
                $('<span><input type="button" value="Modify Quiz"><br></span>').on("click", saveModifiedQuiz));
    }

    function fillFormQuiz(quiz) {
        $("#Qcurrentquestion #quiz-title").val(quiz.title);
        $("#Qcurrentquestion #quiz-uri").val(quiz.id ? `http://127.0.0.1:5000/quizz/api/v1.0/questionnaire/${quiz.id}` : '');
    }

    function saveNewQuiz() {
        const quiz = new Questionnaire(
            null,
            $("#Qcurrentquestion #quiz-title").val(),
            []
        );
        fetch("http://127.0.0.1:5000/quizz/api/v1.0/questionnaire", {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify({ name: quiz.title, questions: quiz.questions })
        })
        .then(res => {
            if (!res.ok) throw new Error('Save failed: ' + res.status);
            console.log('Save Success');
            refreshQuestionnaire();
            return res.json();
        })
        .catch(err => {
            console.error(err);
            $("#Qcurrentquestion").append($('<span>').text('Erreur lors de la sauvegarde'));
        });
    }

    function saveModifiedQuiz() {
        const quiz = new Questionnaire(
            null,
            $("#Qcurrentquestion #quiz-title").val(),
            []
        );
        const uri = $("#Qcurrentquestion #quiz-uri").val();
        fetch(uri, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "PUT",
            body: JSON.stringify({ name: quiz.title })
        })
        .then(res => {
            if (!res.ok) throw new Error('Update failed: ' + res.status);
            console.log('Update Success');
            refreshQuestionnaire();
            return res.json();
        })
        .catch(err => {
            console.error(err);
            $("#Qcurrentquestion").append($('<span>').text('Erreur lors de la modification'));
        });
    }

    $("#Qtool #QdelQuiz").on('click', delQuiz);

    function delQuiz() {
        const url = $("#Qcurrentquestion #quiz-uri").val();
        if (url) {
            fetch(url, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                method: "DELETE"
            })
            .then(res => {
                if (!res.ok) throw new Error('Delete failed: ' + res.status);
                console.log('Delete Success');
                refreshQuestionnaire();
            })
            .catch(err => {
                console.error(err);
                $("#Qcurrentquestion").append($('<span>').text('Erreur lors de la suppression'));
            });
        }
    }

    // CRUD operations for Question
    let selectedQuestionnaireId = null; // Store selected questionnaire ID

    function formQuestion(isNew = true) {
        $("#Qcurrentquestion").empty();
        $("#Qcurrentquestion")
            .append($('<span>Titre<input type="text" id="question-title"><br></span>'))
            .append($('<span>Réponse<input type="text" id="question-reponse"><br></span>'))
            .append($('<span><input type="hidden" id="question-uri"><br></span>'))
            .append(isNew ?
                $('<span><input type="button" value="Save Question"><br></span>').on("click", saveNewQuestion) :
                $('<span><input type="button" value="Modify Question"><br></span>').on("click", saveModifiedQuestion));
    }

    function fillFormQuestion(question) {
        $("#Qcurrentquestion #question-title").val(question.title);
        $("#Qcurrentquestion #question-reponse").val(question.reponse);
        $("#Qcurrentquestion #question-uri").val(question.id ? `http://127.0.0.1:5000/quizz/api/v1.0/question/${question.id}` : '');
    }

    function saveNewQuestion() {
        const question = new Question(
            null,
            $("#Qcurrentquestion #question-title").val(),
            $("#Qcurrentquestion #question-reponse").val(),
            null
        );
        fetch("http://127.0.0.1:5000/quizz/api/v1.0/question", {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify({ 
                title: question.title, 
                reponse: question.reponse,
                questionnaire_id: selectedQuestionnaireId // Associate with selected questionnaire
            })
        })
        .then(res => {
            if (!res.ok) throw new Error('Save failed: ' + res.status);
            console.log('Save Success');
            fetchQuestionsForQuestionnaire(selectedQuestionnaireId); // Refresh questions for current quiz
            return res.json();
        })
        .catch(err => {
            console.error(err);
            $("#Qcurrentquestion").append($('<span>').text('Erreur lors de la sauvegarde'));
        });
    }

    function saveModifiedQuestion() {
        const question = new Question(
            null,
            $("#Qcurrentquestion #question-title").val(),
            $("#Qcurrentquestion #question-reponse").val(),
            null
        );
        const uri = $("#Qcurrentquestion #question-uri").val();
        fetch(uri, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "PUT",
            body: JSON.stringify({ title: question.title, reponse: question.reponse })
        })
        .then(res => {
            if (!res.ok) throw new Error('Update failed: ' + res.status);
            console.log('Update Success');
            fetchQuestionsForQuestionnaire(selectedQuestionnaireId); // Refresh questions
            return res.json();
        })
        .catch(err => {
            console.error(err);
            $("#Qcurrentquestion").append($('<span>').text('Erreur lors de la modification'));
        });
    }

    $("#Qtool #QdelQuestion").on('click', delQuestion);

    function delQuestion() {
        const url = $("#Qcurrentquestion #question-uri").val();
        if (url) {
            fetch(url, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                method: "DELETE"
            })
            .then(res => {
                if (!res.ok) throw new Error('Delete failed: ' + res.status);
                console.log('Delete Success');
                fetchQuestionsForQuestionnaire(selectedQuestionnaireId); // Refresh questions
            })
            .catch(err => {
                console.error(err);
                $("#Qcurrentquestion").append($('<span>').text('Erreur lors de la suppression'));
            });
        }
    }

    // CRUD operations for Response
    function formResponse(isNew = true) {
        $("#Qcurrentquestion").empty();
        $("#Qcurrentquestion")
            .append($('<span>Texte<input type="text" id="response-text"><br></span>'))
            .append($('<span><input type="hidden" id="response-uri"><br></span>'))
            .append(isNew ?
                $('<span><input type="button" value="Save Response"><br></span>').on("click", saveNewResponse) :
                $('<span><input type="button" value="Modify Response"><br></span>').on("click", saveModifiedResponse));
    }

    function fillFormResponse(response) {
        $("#Qcurrentquestion #response-text").val(response.text);
        $("#Qcurrentquestion #response-uri").val(response.id ? `http://127.0.0.1:5000/quizz/api/v1.0/reponse/${response.id}` : '');
    }

    function saveNewResponse() {
        const response = new Response(
            $("#Qcurrentquestion #response-text").val()
        );
        const questionUri = $("#Qcurrentquestion #question-uri").val();
        if (questionUri) {
            const questionId = questionUri.split('/').pop(); // Extract question ID from URI
            fetch(`http://127.0.0.1:5000/quizz/api/v1.0/questions/${questionId}/${response.text}`, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                method: "POST"
            })
            .then(res => {
                if (!res.ok) throw new Error('Save failed: ' + res.status);
                console.log('Save Success');
                fetchQuestionsForQuestionnaire(selectedQuestionnaireId); // Refresh questions
                return res.json();
            })
            .catch(err => {
                console.error(err);
                $("#Qcurrentquestion").append($('<span>').text('Erreur lors de la sauvegarde'));
            });
        } else {
            $("#Qcurrentquestion").append($('<span>').text('Veuillez sélectionner une question d’abord'));
        }
    }

    function saveModifiedResponse() {
        const response = new Response(
            $("#Qcurrentquestion #response-text").val()
        );
        const uri = $("#Qcurrentquestion #response-uri").val();
        fetch(uri, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "PUT",
            body: JSON.stringify({ reponse: response.text })
        })
        .then(res => {
            if (!res.ok) throw new Error('Update failed: ' + res.status);
            console.log('Update Success');
            fetchQuestionsForQuestionnaire(selectedQuestionnaireId); // Refresh questions
            return res.json();
        })
        .catch(err => {
            console.error(err);
            $("#Qcurrentquestion").append($('<span>').text('Erreur lors de la modification'));
        });
    }

    $("#Qtool #Qdel").on('click', delResponse);

    function delResponse() {
        const url = $("#Qcurrentquestion #response-uri").val();
        if (url) {
            fetch(url, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                method: "DELETE"
            })
            .then(res => {
                if (!res.ok) throw new Error('Delete failed: ' + res.status);
                console.log('Delete Success');
                fetchQuestionsForQuestionnaire(selectedQuestionnaireId); // Refresh questions
            })
            .catch(err => {
                console.error(err);
                $("#Qcurrentquestion").append($('<span>').text('Erreur lors de la suppression'));
            });
        }
    }

    // Update editQuiz to store selected questionnaire ID
    function editQuiz(event) {
        $("#Qcurrentquestion").empty();
        formQuiz(false);
        fillFormQuiz(event.data);
        selectedQuestionnaireId = event.data.id; // Store selected questionnaire ID
        fetchQuestionsForQuestionnaire(event.data.id);
    }

    class Questionnaire {
        constructor(id, title, questions) {
            this.id = id;
            this.title = title;
            this.questions = questions || [];
        }
    }

    class Question {
        constructor(id, title, reponse, user) {
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