responses = []

from flask import Flask,request,render_template,redirect,flash

from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey

app = Flask(__name__)

app.config["SECRET_KEY"] = "OH IT'S A SECRET"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def home():
    total_ques = len(satisfaction_survey.questions)
    answer_len = len(responses)
    finish = total_ques == answer_len
    return render_template("home.html",title=satisfaction_survey.title,instruction=satisfaction_survey.instructions,finish=finish)

@app.route("/questions/<int:id>")
def the_question(id):
    total_ques = len(satisfaction_survey.questions)
    answer_len = len(responses)
    if id == answer_len:
        if id < total_ques:
            question = satisfaction_survey.questions[id].question
            choice = satisfaction_survey.questions[id].choices
            return render_template("question.html",question=question,id=id,choice=choice)
        else:
            return redirect("/thanks")
    else:
        if id > total_ques:
            flash("Don't even try,go to beggining one first!")
        return redirect(f"/questions/{answer_len}")

@app.route("/thanks")
def thanks():
    return render_template("thanks.html")

@app.route("/answer/<int:id>",methods=["POST"])
def get_answer(id):
    answer = request.form["answer"]
    responses.append(answer)
    total_ques = len(satisfaction_survey.questions)
    return redirect(f"/questions/{len(responses) + 1}")