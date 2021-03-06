from unicodedata import name
from flask import Flask, make_response, redirect, render_template, request, url_for
from .models import Answers, Customers, Options, db, Questions
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)

    app.config.update(
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{app.instance_path}/survey.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)

    @app.route('/')
    @app.route('/survey')
    def index():
        return render_template('index.html')
    
    @app.route('/survey/report')
    def get_report():
        return render_template('report/index.html')

    @app.route('/survey/form', methods=['GET', 'POST'])
    def form_survey():
        questions = Questions.query.all()
        
        if request.method == 'POST':
            customers_id = request.form['customers_id']
            
            for i in questions:
                questions_id = request.form['questions_'+str(i.id)]
                for j in i.options:
                    options_id = request.form['options_id']
                        
                    answer = Answers(questions_id = questions_id, options_id = options_id, customers_id = customers_id)
                    
                    db.session.add(answer)
                    db.session.commit()
                
                    
            return redirect(url_for('get_report'))
        else:
            return render_template('survey/form.html', questions = questions)

    @app.route('/survey/information', methods=['GET', 'POST'])
    def form_information():
        questions = Questions.query.all()
        customer_id = 0
        
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            age = request.form['age']
            career = request.form['career']
            income = request.form['income']
            
            customer = Customers(name = name, email = email, age = age, career = career,  income = income)
            
            db.session.add(customer)
            db.session.commit()
            
            customer_id = customer.id
            return render_template('survey/form.html',questions = questions, customer_id=customer_id)
        else:
            return render_template('survey/information.html')

    @app.route('/survey/questions')
    def get_survey_question():
        questions = Questions.query.all()

        return render_template('questions/list-question.html', questions=questions)

    @app.route('/survey/questions/form-question/<int:id>', methods=['GET', 'POST'])
    def form_question(id):
        title = ''

        if id:
            title = 'Edit Questions'
        else:
            title = 'Add Questions'

        question = {
            'id': 0,
            'name': '',
            'type': ''
        }

        find_question = Questions.query.filter_by(
            id=id).first()

        if find_question:
            question = find_question
        else:
            question = question

        if request.method == 'POST':
            if id:
                question.name = request.form['name']
                question.type = request.form['type']
                db.session.commit()
                return redirect(url_for('get_survey_question'))
            else:
                name = request.form['name']
                type = request.form['type']
                question = Questions(name=name, type=type)
                db.session.add(question)
                db.session.commit()
                return redirect(url_for('get_survey_question'))
        else:
            return render_template('questions/form-question.html', question=question, title=title)

    @app.route('/survey/questions/remove_question/<int:id>')
    def remove_question(id):
        question = Questions.query.filter_by(id=id).first()
        db.session.delete(question)
        db.session.commit()
        return redirect(url_for('get_survey_question'))

    @app.route('/survey/answers')
    def get_survey_answer():
        answers = Options.query.all()

        return render_template('answers/list-answers.html', answers=answers)

    @app.route('/survey/answers/form-answer/<int:id>', methods=['GET', 'POST'])
    def form_answer(id):
        title = ''

        if id:
            title = 'Edit Answer'
        else:
            title = 'Add Answer'

        answer = {
            'id': 0,
            'name': '',
            'questions_id': 0,
            'questions': {
                'id': 0,
                'name': ''
            }
        }

        find_answer = Options.query.filter_by(
            id=id).first()

        if find_answer:
            answer = find_answer
        else:
            answer = answer

        questions = Questions.query.all()

        if request.method == 'POST':
            if id:
                answer.name = request.form['name']
                db.session.commit()
                return redirect(url_for('get_survey_answer'))
            else:
                name = request.form['name']
                questions_id = request.form['questions_id']
                answer = Options(name=name, questions_id=questions_id)
                db.session.add(answer)
                db.session.commit()
                return redirect(url_for('get_survey_answer'))
        else:
            return render_template('answers/form-answer.html', answer=answer, questions=questions, title=title)

    @app.route('/survey/answers/remove_answer/<int:id>')
    def remove_answer(id):
        answer = Answers.query.filter_by(id=id).first()
        db.session.delete(answer)
        db.session.commit()
        return redirect(url_for('get_survey_answer'))
    return app
