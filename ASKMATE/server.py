from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt

import util
import connection

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'SECRET_KEY'


def password_is_like_password_in_db(pw_from_db, pw_from_user):
    if bcrypt.check_password_hash(pw_from_db, pw_from_user):
        return True
    else:
        pass


def hash_password(password):
    hash_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    return hash_pw


def check_if_mail_is_in_db(user_email):
    if connection.mail_is_in_db(user_email):
        return True
    else:
        return False


@app.route("/latest_five_questions")
def get_5_latest_questions():
    questions = connection.get_five_latest_questions()
    return render_template("list.html",
                           questions=questions,
                           title="Main page")


@app.route("/list")
def display_questions_list():
    order_by_options = {'submission_time': 'Submission time', 'view_number': 'View number',
                        'vote_number': 'Vote number', 'title': 'Title'}
    order_options = ['DESC', 'ASC']
    order_by = request.args.get('order_by')
    order = request.args.get('order')
    questions_list = util.order_questions(order_by, order)

    return render_template("list.html",
                           questions=questions_list,
                           title="List questions",
                           select_options=order_by_options,
                           order_options=order_options,
                           order_by=order_by,
                           order=order)


@app.route('/question/<question_id>')
def display_single_question(question_id):
    single_question = connection.get_question_by_id(question_id)
    headers = ["ID", "SUBMISSION TIME", "VIEW NUMBER", "VOTE NUMBER", "TITLE", "MESSAGE", "IMAGE"]
    answer_headers = ["ID", "SUBMISSION TIME", "VOTE NUMBER", "QUESTION ID", "MESSAGE", "IMAGE"]
    answers_to_single_question = connection.get_answers_by_question_id(question_id)
    comment_to_question = connection.get_comment_for_question(question_id)
    comment_to_answer = connection.get_comment_for_answer(question_id)
    all_tags = connection.get_all_tags()
    tags_assigned_to_question = connection.get_tags_for_question(question_id)
    return render_template('single_question.html', question_id=question_id,
                           single_question=single_question, headers=headers,
                           answer_headers=answer_headers, answers_to_single_question=answers_to_single_question,
                           comment_to_question=comment_to_question, comment_to_answer=comment_to_answer,
                           all_tags=all_tags, tags_assigned_to_question=tags_assigned_to_question)


@app.route('/add_new_question', methods=['POST', 'GET'])
def add_new_question():
    if request.method == 'GET':
        return render_template('add_question.html')
    if request.method == 'POST':
        #session.get czy session['']
        user_email = session.get('user_email')
        user_ID_for_question = connection.get_user_id_for_email(user_email)

        question = {'submission_time': connection.get_submission_time(), 'view_number': 0,
                    'vote_number': 0, 'title': request.form.get('title'),
                    'message': request.form.get('message'), 'image': None, 'user_ID_for_question': user_ID_for_question}
        connection.insert_question_to_database(question)

        return redirect(url_for('display_questions_list'))


@app.route('/question/<question_id>/add_new_answer', methods=['POST', 'GET'])
def add_new_answer(question_id):
    if request.method == 'GET':
        return render_template('add_answer.html', question_id=question_id)
    if request.method == 'POST':
        user_email = session.get('user_email')
        user_ID_for_question = connection.get_user_id_for_email(user_email)

        answer = {'submission_time': connection.get_submission_time(), 'vote_number': 0,
                  'question_id': question_id, 'message': request.form.get('message'),
                  'image': request.form.get('image'), 'user_id_for_answer': user_ID_for_question}
        connection.insert_answer_to_database(answer)
        return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/question/<question_id>/delete', methods=["POST"])
def delete_question(question_id):
    connection.delete_question_from_database(question_id)
    return redirect(url_for('display_questions_list', question_id=question_id))


@app.route('/question/<question_id>/delete', methods=["GET"])
def confirm_delete_question(question_id):
    return render_template("confirm_delete_question.html", question_id=question_id)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    question_id = request.args.get('question_id')
    connection.delete_answer_from_database(answer_id)
    return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/question/<question_id>/edit', methods=["POST", "GET"])
def update_question(question_id):
    if request.method == 'GET':
        title_content = connection.get_question_by_id(question_id)["title"]
        question_content = connection.get_question_by_id(question_id)["message"]
        return render_template('edit_question.html', question_id=question_id, question_content=question_content,
                               title_content=title_content)
    elif request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        connection.update_question_in_database(title, message, question_id)
        return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/answer/<answer_id>/edit', methods=["POST", "GET"])
def update_answer(answer_id):
    if request.method == 'GET':
        answer_content = connection.get_answer_by_id(answer_id)["message"]
        return render_template('edit_answer.html', answer_id=answer_id, answer_content=answer_content)
    elif request.method == 'POST':
        question_id = request.args.get('question_id')
        message = request.form.get('message')
        connection.update_answer_in_database(message, answer_id)
        return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/comment/<comment_id>/edit', methods=["POST", "GET"])
def update_comment(comment_id):
    if request.method == 'GET':
        comment_content = connection.get_comment_by_id(comment_id)["message"]
        return render_template('edit_comment.html', comment_id=comment_id, comment_content=comment_content)
    elif request.method == 'POST':
        question_id = request.args.get('question_id')
        message = request.form.get('message')
        connection.update_comment_in_database(message, comment_id)
        return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/comments/<comment_id>/delete')
def delete_comment(comment_id):
    connection.delete_comment_from_database(comment_id)
    question_id = request.args.get('question_id')
    return redirect(url_for('display_single_question', comment_id=comment_id, question_id=question_id))


@app.route('/question/<int:question_id>/vote')
def vote_for_question(question_id):
    vote_type = request.args.get('vote_type')
    vote_number = connection.get_vote_number_question(question_id)
    vote_up_or_down = util.vote_up_or_down(vote_number, vote_type)
    connection.update_vote_number_question(vote_up_or_down, question_id)
    return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/answer/<answer_id>/vote', methods=["GET"])
def vote_for_answer(answer_id):
    question_id = request.args.get('question_id')
    vote_type = request.args.get('vote_type')
    vote_number = connection.get_vote_number_answer(answer_id)
    vote_up_or_down = util.vote_up_or_down(vote_number, vote_type)
    connection.update_vote_number_answer(vote_up_or_down, answer_id)
    return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/question/<question_id>/new-comment', methods=["GET", "POST"])
def add_comment_to_question(question_id):
    if request.method == 'GET':
        return render_template('add_comment_for_question.html', question_id=question_id)
    if request.method == 'POST':
        user_mail = session.get('user_email')
        user_id = connection.get_user_id_for_email(user_mail)
        new_comment = {'question_id': question_id, 'answer_id': None,
                       'message': request.form.get('message'), 'submission_time': connection.get_submission_time(),
                       'edited_count': 0, 'user_id_for_comment': user_id}
        connection.insert_comment_question_to_database(new_comment)
    return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/answer/<answer_id>/new-comment', methods=["GET", "POST"])
def add_comment_to_answer(answer_id):
    question_id = request.args.get("question_id")
    if request.method == 'GET':
        return render_template('add_comment_for_answer.html', answer_id=answer_id, question_id=question_id)
    if request.method == 'POST':
        new_comment = {
            'question_id': question_id,
            'answer_id': answer_id,
            'message': request.form.get('message'),
            'submission_time': connection.get_submission_time(),
            'edited_count': 0
        }
        connection.insert_comment_answer_to_database(new_comment)

        return redirect(url_for('display_single_question',
                                question_id=question_id,
                                ))


@app.route('/question/<int:question_id>/new-tag', methods=["GET", "POST"])
def add_tag(question_id: int):
    if request.method == 'GET':
        all_tags = connection.get_all_tags()
        return render_template('create_tag.html', question_id=question_id, all_tags=all_tags)
    if request.method == 'POST':
        new_tag = {'name': request.form.get('tag')}
        connection.insert_question_tag_to_database(new_tag)
        return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/question/<question_id>/link-question-with-tag', methods=["POST"])
def add_connection(question_id):
    tags_for_question = {'question_id': question_id, 'tag_id': request.form.get('tag-id')}
    connection.insert_association_to_tag(tags_for_question)
    return redirect(url_for('display_single_question', question_id=question_id, tags_for_question=tags_for_question))


@app.route('/question/<question_id>', methods=["POST"])
def get_tags_for_question(question_id):
    tags_assigned_to_question = connection.get_tags_for_question(question_id)
    return render_template('single_question.html', question_id=question_id,
                           tags_assigned_to_question=tags_assigned_to_question)


@app.route('/question/<question_id>/delete_tag', methods=["POST"])
def delete_tag(question_id: int):
    tags_for_delete = {'question_id': question_id, 'tag_id': request.form.get('tag-id')}
    connection.delete_tag_for_question(tags_for_delete)
    return redirect(url_for('display_single_question', question_id=question_id, tags_for_delete=tags_for_delete))


@app.route('/search')
def question_list_by_phrase():
    phrase = request.args.get('phrase')

    if phrase:
        questions = connection.get_question_by_phrase(phrase)
    else:
        return redirect(url_for('index'))

    return render_template('list.html', questions=questions)


@app.route('/')
def first_page():
    return render_template('first_page.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        password = request.form.get('password')
        hashed_password = hash_password(password)
        user_data = {'user_name': request.form.get('user_name'), 'password': hashed_password,
                     'email': request.form.get('email'), 'registration_date': connection.get_register_time()}
        # 'aked_questions': connection.count_asked_questions() TO NA GÓRĘ żeby dodać do tabelki
        connection.register_user(user_data)
        return render_template('first_page.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        hash_password = connection.get_hashpw_by_email(user_email)

        session['user_email'] = request.form.get('email')

        if check_if_mail_is_in_db(user_email) and password_is_like_password_in_db(hash_password, user_password):
            return redirect(url_for('display_questions_list'))
        else:
            session.pop('user_email', None)
            return render_template('first_page.html')

@app.route('/logout', methods=['GET'])
def log_out():
    session.pop('user_email', None)
    return redirect(url_for('first_page'))

@app.route('/user_list', methods = ['GET'])
def user_list():
    headers = ['user id', 'user name']
    users_data = connection.get_users()
    return render_template('user_list.html', users_data=users_data, headers=headers)






if __name__ == "__main__":
    app.debug = True
    app.run()
    app.run(
        host='localhost',
        port=5000,
        debug=True,
    )
