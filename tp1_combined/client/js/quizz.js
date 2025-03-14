$(function() {
    const apiBaseUrl = 'http://127.0.0.1:5000/quizz/api/v1.0';

    $("#Qbutton").click(refreshQuestionnaire);
    $("#Qtool #QaddQuiz").click(() => formQuiz(true));
    $("#Qtool #QdelQuiz").click(delQuiz);
    $("#Qtools #QaddQuestion").click(() => formQuestion(true));
    $("#Qtools #QdelQuestion").click(delQuestion);

    function refreshQuestionnaire() {
        $("#Qcurrentquestion").empty();
        $("#Qcurrentquestion2").empty();
        fetch(`${apiBaseUrl}/questionnaire`)
            .then(response => {
                if (!response.ok) throw new Error('AJAX Error: ' + response.status);
                return response.json();
            })
            .then(fillListQuestionnaire)
            .catch(err => {
                console.error(err);
                $("#Qquestionnaires").html("<b>Impossible de récupérer les Questionnaires</b>" + err);
            });
    }

    function fillListQuestionnaire(repjson) {
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

    function editQuiz(event) {
        const quiz = event.data;
        $("#Qcurrentquestion").empty();
        $("#Qcurrentquestion").append(`
            <h3>${quiz.title}</h3>
        `);
        formQuiz(false, quiz);
        selectedQuestionnaireId = quiz.id;
        fetchQuestionsForQuestionnaire(quiz.id);
    }

    function fetchQuestionsForQuestionnaire(quizId) {
        // $("#Qcurrentquestion2").empty();
        fetch(`${apiBaseUrl}/questionnaire/${quizId}`)
            .then(response => {
                if (!response.ok) throw new Error('AJAX Error: ' + response.status);
                return response.json();
            })
            .then(fillListQuestion)
            .catch(err => {
                console.error(err);
                $("#Qcurrentquestion").html("<b>Impossible de récupérer les Questions du Questionnaire</b>" + err);
            });
    }

    function fillListQuestion(repjson) {
        console.log("fillListQuestion",repjson);
        // $('#Qcurrentquestion').empty();
        $('#Qcurrentquestion').append($('<ul>'));
        for (let index = 0; index < repjson.questionnaire.questions.length; index++) {
            const questionData = repjson.questionnaire.questions[index];
            const question = new Question(questionData.id, questionData.title, questionData.reponse);
            console.log(question);
            $('#Qcurrentquestion ul')
                .append($('<li>')
                    .append($('<a>')
                        .text(question.title)
                    ).on("click", question, highlightAndEditQuestion)
                );
        }
    }

    function highlightAndEditQuestion(event) {
        console.log(event.target);
        const question = event.data;
        $("#Qcurrentquestion2").empty();
        $("#Qcurrentquestion2").append(`
            <h4>${question.title}</h4>
            <p>Réponse: ${question.reponse}</p>
        `);
        formQuestion(false, question);
    }

    function formQuiz(isNew = true, quiz = null) {
        $("#Qcurrentquestion").empty();
        $("#Qcurrentquestion")
            .append($('<span>Titre<input type="text" id="quiz-title"><br></span>'))
            .append($('<span><input type="hidden" id="quiz-uri"><br></span>'))
            .append(isNew ?
                $('<span><input type="button" value="Save Quiz"><br></span>').on("click", saveNewQuiz) :
                $('<span><input type="button" value="Modify Quiz"><br></span>').on("click", saveModifiedQuiz));

        if (!isNew && quiz) {
            $("#quiz-title").val(quiz.title);
            $("#quiz-uri").val(quiz.id ? `${apiBaseUrl}/questionnaire/${quiz.id}` : '');
        }
    }

    function saveNewQuiz() {
        const quiz = {
            title: $("#quiz-title").val(),
            questions: []
        };
        fetch(`${apiBaseUrl}/questionnaire`, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify(quiz)
        })
        .then(res => {
            if (!res.ok) throw new Error('Save failed: ' + res.status);
            console.log('Save Success');
            refreshQuestionnaire();
        })
        .catch(err => {
            console.error(err);
            $("#Qcurrentquestion").append($('<span>').text('Erreur lors de la sauvegarde'));
        });
    }

    function saveModifiedQuiz() {
        const quiz = {
            name: $("#quiz-title").val()
        };
        const uri = $("#quiz-uri").val();
        fetch(uri, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "PUT",
            body: JSON.stringify(quiz)
        })
        .then(res => {
            if (!res.ok) throw new Error('Update failed: ' + res.status);
            console.log('Update Success');
            refreshQuestionnaire();
        })
        .catch(err => {
            console.error(err);
            $("#Qcurrentquestion").append($('<span>').text('Erreur lors de la modification'));
        });
    }

    function delQuiz() {
        const url = $("#quiz-uri").val();
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
                $("#Qcurrentquestion2").append($('<span>').text('Erreur lors de la suppression'));
            });
        }
    }

    let selectedQuestionnaireId = null;

    function formQuestion(isNew = true, question = null) {
        $("#Qcurrentquestion2").empty();
        $("#Qcurrentquestion2")
            .append($('<span>Titre<input type="text" id="question-title"><br></span>'))
            .append($('<span>Réponse<input type="text" id="question-reponse"><br></span>'))
            .append($('<span><input type="hidden" id="question-uri"><br></span>'))
            .append(isNew ?
                $('<span><input type="button" value="Save Question"><br></span>').on("click", saveNewQuestion) :
                $('<span><input type="button" value="Modify Question"><br></span>').on("click", saveModifiedQuestion));

        if (!isNew && question) {
            $("#question-title").val(question.title);
            $("#question-reponse").val(question.reponse);
            $("#question-uri").val(question.id ? `${apiBaseUrl}/question/${question.id}` : '');
        }
    }

    function saveNewQuestion() {
        const question = {
            title: $("#question-title").val(),
            reponse: $("#question-reponse").val(),
            questionnaire_id: selectedQuestionnaireId
        };
        fetch(`${apiBaseUrl}/question`, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify(question)
        })
        .then(res => {
            if (!res.ok) throw new Error('Save failed: ' + res.status);
            console.log('Save Success');
            fetchQuestionsForQuestionnaire(selectedQuestionnaireId);
        })
        .catch(err => {
            console.error(err);
            $("#Qcurrentquestion2").append($('<span>').text('Erreur lors de la sauvegarde'));
        });
    }

    function saveModifiedQuestion() {
        const question = {
            title: $("#question-title").val(),
            reponse: $("#question-reponse").val()
        };
        const uri = $("#question-uri").val();
        fetch(uri, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "PUT",
            body: JSON.stringify(question)
        })
        .then(res => {
            if (!res.ok) throw new Error('Update failed: ' + res.status);
            console.log('Update Success');
            fetchQuestionsForQuestionnaire(selectedQuestionnaireId);
        })
        .catch(err => {
            console.error(err);
            $("#Qcurrentquestion2").append($('<span>').text('Erreur lors de la modification'));
        });
    }

    function delQuestion() {
        const url = $("#question-uri").val();
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
                fetchQuestionsForQuestionnaire(selectedQuestionnaireId);
            })
            .catch(err => {
                console.error(err);
                $("#Qcurrentquestion2").append($('<span>').text('Erreur lors de la suppression'));
            });
        }
    }

    class Questionnaire {
        constructor(id, title, questions) {
            this.id = id;
            this.title = title;
            this.questions = questions || [];
        }
    }

    class Question {
        constructor(id, title, reponse) {
            this.id = id;
            this.title = title;
            this.reponse = reponse;
        }
    }
});
