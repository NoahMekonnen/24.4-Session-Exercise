from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "Godalone1"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def satisfaction_questions():
    return render_template('sat_survey.html',title = satisfaction_survey.title, instructions = satisfaction_survey.instructions)
    
@app.route('/responses', methods=['POST'])
def start_responses():
    session['responses'] = []
    return redirect('/questions/0')

@app.route("/questions/<int:n>")
def give_question(n):
    k = len(session['responses'])
    if k == 4:
        return redirect("/thank_you")
    elif k != n:
        flash("Invalid Question")
        return redirect(f"/questions/{k}")
    return render_template('form.html', question = satisfaction_survey.questions[n].question, choices = satisfaction_survey.questions[n].choices)

@app.route("/answer")
def give_answers():
    answer = request.args['ans']
    session['responses'].append(answer)
    session.modified = True
    if len(session['responses']) < 4:
        return redirect(f"/questions/{(len(session['responses']))%4}")
    return redirect("/thank_you")

@app.route("/thank_you")
def thanks():
    return render_template('thank_you.html')