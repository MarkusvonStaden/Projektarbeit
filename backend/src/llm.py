import os
from ollama import Client
from pydantic import BaseModel

MODEL = os.getenv("LLM_MODEL", "gemma3:1b")
HOST = os.getenv("OLLAMA_HOST", "localhost")

ollama = Client(host=f"http://{HOST}:11434")

models = ollama.list().get("models", [])
if MODEL not in models:
    ollama.pull(MODEL)


class Answer(BaseModel):
    isAnswered: bool
    answer: str
    

def response_answers_question(question: str, responses: list[str]) -> str | None:
    model = MODEL
    prompt = f"Is the following question answered by the provided question-answer pairs? If yes, provide the answer. If not, respond with an empty string.\n\n<question> {question} </question>\n<previousAnswers>\n"
    for q, a in responses:
        prompt += f"<question>\n{q}\n</question>\n<answer>\n{a}\n</answer>\n"
    prompt += "</previousAnswers>\nUse your own words to answer the question. Use the same language as the user. "
    print(f"Prompt: {prompt}")
    response = ollama.generate(
        model=model,
        format=Answer.model_json_schema(),
        prompt=prompt,
        stream=False,
    )
    answer = Answer.model_validate_json(response.response)
    return answer.answer if answer.isAnswered else None

if __name__ == "__main__":
    question = "What color is the car?"
    responses = [
        "The capital of France is Paris.",
        "France is known for its rich history and culture.",
        "Paris is also famous for its landmarks like the Eiffel Tower."
    ]
    
    answer = response_answers_question(question, responses)
    print(f"Is the question answered? {answer.isAnswered}")
    print(f"Answer: {answer.answer}")