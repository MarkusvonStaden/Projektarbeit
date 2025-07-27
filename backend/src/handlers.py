# from db import insert_question, get_question, insert_answer
import stores_dense
import llm
from stores_dense import get_all_questions, get_question_by_id, insert_question, insert_answer, omit_answer, mark_answer_correct

def post_question_handler(*args, **kwargs):
    question = kwargs.get('question', '')
    question_id = insert_question(question)

    results = stores_dense.search(question)
    print(f"Search results for question '{question}': {results}")

    if results:
        answer = llm.response_answers_question(question, results)
        if answer:
            insert_answer(question_id, answer)
    else:
        answer = None


    return {
        "id": question_id,
        "answer": answer,
    }

def get_question_handler(*args, **kwargs):
    return get_question_by_id(kwargs.get('question_id', ''))

def get_questions_handler(*args, **kwargs):
    return get_all_questions()

def omit_answer_handler(*args, **kwargs):
    question_id = kwargs.get('question_id', '')    
    return omit_answer(question_id)

def post_answer_handler(*args, **kwargs):
    question_id = kwargs.get('question', '')
    answer = kwargs.get('answer', '')
    return insert_answer(question_id, answer)

def mark_answer_correct_handler(*args, **kwargs):
    question_id = kwargs.get('question_id', '')
    return mark_answer_correct(question_id)

# def post_answer_handler(*args, **kwargs):
#     question_id = kwargs.get('question', '')
#     answer = kwargs.get('answer', '')
#     question = get_question(question_id).get('question', '') if question_id else ''
#     stores_dense.add_question_answer(question, answer)
#     return insert_answer(question_id, answer) if question_id and answer else False