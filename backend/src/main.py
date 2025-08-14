from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from handlers import post_question_handler, get_questions_handler, get_question_handler, post_answer_handler, omit_answer_handler, mark_answer_correct_handler
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/questions")
async def get_questions():
    return get_questions_handler()


@app.post("/questions")
async def post_question(question: str = Body(...)):
    return post_question_handler(question=question)


@app.get("/questions/{question_id}")
async def get_question(question_id: str):
    return get_question_handler(question_id=question_id)


@app.post("/questions/{question_id}/answer")
async def add_answer(question_id: str, answer: str = Body(...)):
    return post_answer_handler(question=question_id, answer=answer)


@app.post("/questions/{question_id}/omit")
async def omit_answer(question_id: str):
    return omit_answer_handler(question_id=question_id)

@app.post("/questions/{question_id}/correct")
async def mark_correct(question_id: str):
    return mark_answer_correct_handler(question_id=question_id)
