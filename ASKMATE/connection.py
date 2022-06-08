import datetime, common
from psycopg2.extras import RealDictCursor


def get_submission_time():
    time = datetime.datetime.now()
    return time.strftime('%Y-%m-%d %H:%M:%S')


def get_register_time():
    time = datetime.datetime.now()
    return time.strftime('%Y-%m-%d %H:%M:%S')


@common.connection_handler
def get_all_questions(cursor: RealDictCursor):
    query = """
    SELECT * FROM question
    ORDER BY submission_time
    """
    cursor.execute(query)
    return cursor.fetchall()


@common.connection_handler
def get_all_questions(cursor: RealDictCursor, order_by, order):
    query = f"""
    SELECT * FROM question
    ORDER BY {order_by} {order};
    """
    cursor.execute(query)
    return cursor.fetchall()


@common.connection_handler
def get_all_answers(cursor: RealDictCursor):
    query = """
    SELECT * FROM answer
    ORDER BY submission_time
    """
    cursor.execute(query)
    return cursor.fetchall()


@common.connection_handler
def get_question_by_id(cursor: RealDictCursor, id: int):
    query = """
    SELECT * FROM question
    WHERE id=%(id)s
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchone()


@common.connection_handler
def get_answer_by_id(cursor: RealDictCursor, id: int):
    query = """
    SELECT * FROM answer
    WHERE id=%(id)s
    ORDER BY submission_time
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchone()


@common.connection_handler
def get_answers_by_question_id(cursor: RealDictCursor, id: int):
    query = """
    SELECT * FROM answer
    WHERE question_id=%(id)s
    ORDER BY submission_time
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchall()


@common.connection_handler
def insert_question_to_database(cursor: RealDictCursor, question: dict):
    query = """
            INSERT INTO question (submission_time, title, message, vote_number, view_number, user_ID_for_question)
            VALUES (%(submission_time)s, %(title)s, %(message)s, %(vote_number)s, %(view_number)s, %(user_ID_for_question)s);
            """
    cursor.execute(query, {
        'submission_time': question['submission_time'],
        'message': question['message'],
        'title': question['title'],
        'vote_number': question['vote_number'],
        'view_number': question['view_number'],
        'user_ID_for_question': question['user_ID_for_question']
    })
    return "QUESTION ADDED"


@common.connection_handler
def insert_answer_to_database(cursor: RealDictCursor, answer: dict):
    query = """
               INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id_for_answer)
               VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s, %(user_id_for_answer)s)
               """
    cursor.execute(query, {
        'submission_time': answer['submission_time'],
        'vote_number': answer['vote_number'],
        'question_id': answer['question_id'],
        'message': answer['message'],
        'image': answer['image'],
        'user_id_for_answer': answer['user_id_for_answer']
    })
    return "ANSWER ADDED"


@common.connection_handler
def delete_question_from_database(cursor: RealDictCursor, id: int):
    query = """
    DELETE FROM question
    WHERE id=%(id)s
    """
    cursor.execute(query, {'id': id})
    return "QUESTION DELETED"


@common.connection_handler
def delete_answer_from_database(cursor: RealDictCursor, id: int):
    query = """
    DELETE FROM answer
    WHERE id=%(id)s
    """
    cursor.execute(query, {'id': id})
    return "ANSWER DELETED"


@common.connection_handler
def delete_comment_from_database(cursor: RealDictCursor, id: int):
    query = """
    DELETE FROM comment
    WHERE id=%(id)s
    """
    cursor.execute(query, {'id': id})
    return "COMMENT DELETED"


@common.connection_handler
def update_question_in_database(cursor: RealDictCursor, title: str, message: str, id: int):
    query = """
    UPDATE question
    SET title = %(title)s, message = %(message)s
    WHERE id=%(id)s
    """
    cursor.execute(query, {'title': title, 'message': message, 'id': id})
    return "QUESTION UPDATED"


@common.connection_handler
def update_answer_in_database(cursor: RealDictCursor, message: str, id: int):
    query = """
    UPDATE answer
    SET submission_time = %(submission_time)s, message = %(message)s
    WHERE id=%(id)s
    """
    cursor.execute(query, {'message': message, 'id': id, 'submission_time': get_submission_time()})
    return "ANSWER UPDATED"


@common.connection_handler
def update_comment_in_database(cursor: RealDictCursor, message: str, id: int) -> list:
    query = """
     UPDATE comment
     SET submission_time = %(submission_time)s, message = %(message)s, edited_count = edited_count + 1
     WHERE id=%(id)s
     """
    cursor.execute(query, {'message': message, 'id': id, 'submission_time': get_submission_time()})
    return "COMMENT UPDATED"


@common.connection_handler
def get_vote_number_question(cursor: RealDictCursor, id: int):
    query = """
    SELECT vote_number FROM question
    WHERE id=%(id)s
    """
    cursor.execute(query, {'id': id})
    vote_number = cursor.fetchall()
    return vote_number[0]


@common.connection_handler
def get_vote_number_answer(cursor: RealDictCursor, id: int):
    query = """
    SELECT vote_number FROM answer
    WHERE id=%(id)s
    """
    cursor.execute(query, {'id': id})
    vote_number = cursor.fetchall()
    return vote_number[0]


@common.connection_handler
def update_vote_number_question(cursor: RealDictCursor, vote_number, id: int):
    query = """
    UPDATE question
    SET vote_number = %(vote_number)s
    WHERE id = %(id)s
    """
    cursor.execute(query, {'vote_number': vote_number, 'id': id})
    return "VOTE NUMBER UPDATED"


@common.connection_handler
def update_vote_number_answer(cursor: RealDictCursor, vote_number, id: int):
    query = """
    UPDATE answer
    SET vote_number = %(vote_number)s
    WHERE id = %(id)s
    """
    cursor.execute(query, {'vote_number': vote_number, 'id': id})
    return "VOTE NUMBER UPDATED"


@common.connection_handler
def get_comment_for_question(cursor: RealDictCursor, question_id):
    query = """
    SELECT * FROM comment
    WHERE question_id=%(question_id)s
    and answer_id is null
    """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@common.connection_handler
def insert_comment_question_to_database(cursor: RealDictCursor, comment_to_question: dict):
    query = """
    INSERT INTO comment(question_id, answer_id, message, submission_time, edited_count, user_id_for_comment)
    VALUES (%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s, %(user_id_for_comment)s)
    """
    cursor.execute(query, {
        'question_id': comment_to_question['question_id'],
        'answer_id': comment_to_question['answer_id'],
        'message': comment_to_question['message'],
        'submission_time': comment_to_question['submission_time'],
        'edited_count': comment_to_question['edited_count'],
        'user_id_for_comment': comment_to_question['user_id_for_comment']
    })
    return "COMMENT ADDED"


@common.connection_handler
def get_comment_for_answer(cursor: RealDictCursor, question_id):
    query = """
    SELECT * FROM comment
    WHERE answer_id is NOT null
    and question_id = %(question_id)s
    """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@common.connection_handler
def get_comment_by_id(cursor: RealDictCursor, comment_id: int):
    query = """
    SELECT * FROM comment
    WHERE id = %(comment_id)s
    """
    cursor.execute(query, {'comment_id': comment_id})
    return cursor.fetchone()


@common.connection_handler
def insert_comment_answer_to_database(cursor: RealDictCursor, new_comment: dict):
    query = """
    INSERT INTO comment(question_id, answer_id, message, submission_time, edited_count)
    VALUES (%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s)
    """
    cursor.execute(query, {
        'question_id': new_comment['question_id'],
        'answer_id': new_comment['answer_id'],
        'message': new_comment['message'],
        'submission_time': new_comment['submission_time'],
        'edited_count': new_comment['edited_count']
    })
    return "COMMENT ADDED"


@common.connection_handler
def get_five_latest_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time DESC
                    LIMIT 5;
                    """)
    questions = cursor.fetchall()
    return questions


@common.connection_handler
def get_question_by_phrase(cursor, phrase):
    cursor.execute("""
                            SELECT * FROM question
                            WHERE LOWER(title) LIKE LOWER(%(phrase)s) 
                            OR LOWER(message) LIKE LOWER(%(phrase)s);
                            """,
                   {'phrase': '%' + phrase + '%'})
    return cursor.fetchall()


@common.connection_handler
def insert_question_tag_to_database(cursor: RealDictCursor, new_tag: dict):
    query = """
        INSERT INTO tag(name)
        VALUES (%(name)s)
        """
    cursor.execute(query, {'name': new_tag['name']})
    return "TAG HAS BEEN ADDED"


@common.connection_handler
def get_all_tags(cursor: RealDictCursor):
    query = """
    SELECT * FROM tag
    """
    cursor.execute(query)
    return cursor.fetchall()


@common.connection_handler
def insert_association_to_tag(cursor: RealDictCursor, tags_for_question: dict):
    query = '''
        INSERT INTO question_tag(question_id, tag_id)
        VALUES (%(question_id)s, %(tag_id)s)
    '''
    cursor.execute(query, {
        'question_id': tags_for_question['question_id'],
        'tag_id': tags_for_question['tag_id']
    })
    return "you have assigned a tag to the question"


@common.connection_handler
def get_tags_for_question(cursor: RealDictCursor, question_id: int):
    query = """
    SELECT * FROM tag JOIN question_tag ON tag.id = question_tag.tag_id WHERE question_id=%(question_id)s
    """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@common.connection_handler
def delete_tag_for_question(cursor: RealDictCursor, tags_for_delete: dict):
    query = '''
    DELETE FROM question_tag
    WHERE tag_id = %(tag_id)s AND question_id = %(question_id)s
    '''
    cursor.execute(query, {'question_id': tags_for_delete['question_id'], 'tag_id': tags_for_delete['tag_id']})
    return 'tag has been deleted'


@common.connection_handler
def get_question_by_phrase(cursor, phrase):
    cursor.execute("""
                            SELECT * FROM question
                            WHERE LOWER(title) LIKE LOWER(%(phrase)s) 
                            OR LOWER(message) LIKE LOWER(%(phrase)s);
                            """,
                   {'phrase': '%' + phrase + '%'})
    return cursor.fetchall()


# @common.connection_handler
# def count_asked_questions()

@common.connection_handler
def register_user(cursor: RealDictCursor, user_data: dict):
    query = '''INSERT INTO user_data (user_name, password, email, registration_date) 
                VALUES (%(user_name)s, %(password)s, %(email)s, %(registration_date)s)'''

    cursor.execute(query, {
        'user_name': user_data['user_name'],
        'password': user_data['password'],
        'email': user_data['email'],
        'registration_date': user_data['registration_date']
    })
    return 'New profile has been created'


@common.connection_handler
def mail_is_in_db(cursor: RealDictCursor, user_email: str):
    # function in main returs True if mails is in DB or False if not
    query = '''SELECT * FROM user_data WHERE email=%(user_email)s '''

    cursor.execute(query, {'user_email': user_email})
    return cursor.fetchone()


@common.connection_handler
def get_hashpw_by_email(cursor: RealDictCursor, user_email: str):
    query = '''SELECT password FROM user_data WHERE email=%(user_email)s'''

    cursor.execute(query, {'user_email': user_email})
    dict_with_has_pw = cursor.fetchall()
    if dict_with_has_pw:
        only_hash_pw = dict_with_has_pw[0]['password']
        return only_hash_pw
    else:
        return False


@common.connection_handler
def get_user_id_for_email(cursor: RealDictCursor, user_email: str):
    query = '''SELECT ID FROM user_data WHERE email=%(user_email)s'''

    cursor.execute(query, {'user_email': user_email})
    id_in_dict = cursor.fetchall()
    only_id = id_in_dict[0]['id']
    return only_id


# @common.connection_handler
# def get_user_name_for_email(cursor: RealDictCursor, user_id: int):
#     query = '''SELECT user_name FROM user_data WHERE id=%(user_id)s '''
#
#     cursor.execute(query, {'user_id': user_id})
#     user_name_in_dict = cursor.fetchall()
#     only_user_name = user_name_in_dict[0]['user_name']
#
#     return only_user_name

@common.connection_handler
def get_users(cursor: RealDictCursor):
    query = '''SELECT id, user_name FROM user_data'''

    cursor.execute(query)
    return cursor.fetchall()
