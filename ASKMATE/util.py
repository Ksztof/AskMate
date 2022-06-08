import connection


def order_questions(order_by, order):
    if order is not None:
        questions = connection.get_all_questions(order_by, order)
    else:
        order_by = 'submission_time'
        order = 'DESC'
        questions = connection.get_all_questions(order_by, order)
    return questions


def vote_up_or_down(vote_number, vote_type):
    if vote_type == 'up':
        vote_number['vote_number'] += 1
    else:
        vote_number['vote_number'] -= 1
    return vote_number['vote_number']

