import os
from ollama import Client
from pydantic import BaseModel

MODEL = os.getenv("LLM_MODEL", "deepseek-r1:32b")
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
    prompt = f"""You are an intelligent assistant that analyzes whether a question can be answered from provided question-answer pairs.

TASK:
Determine if the given question can be answered using the information from the previous question-answer pairs.

QUESTION TO ANALYZE:
{question}

AVAILABLE QUESTION-ANSWER PAIRS:
"""
    for i, (q, a) in enumerate(responses, 1):
        prompt += f"{i}. Question: {q}\n   Answer: {a}\n\n"
    
    prompt += """INSTRUCTIONS:
1. Carefully analyze if any of the provided answers contain information that answers the given question
2. If the question CAN be answered:
   - Set "isAnswered" to true
   - Provide a clear, concise answer in the "answer" field using your own words
   - Use the same language as the original question
3. If the question CANNOT be answered:
   - Set "isAnswered" to false
   - Set "answer" to an empty string

IMPORTANT:
- Only answer if you can provide a meaningful response based on the available information
- Do not make assumptions or add information not present in the provided answers
- Maintain the same language and tone as the original question. If the Question to Analyze is in English, the answer should also be in English and so on.
- MUST output valid JSON only - no additional text, explanations, or formatting outside the JSON structure
- Do NOT include any formatting like newlines, bullet points, or lists in the JSON output
- Do NOT add opening brackets or any text before the JSON"""

    response = ollama.generate(
        model=model,
        format=Answer.model_json_schema(),
        prompt=prompt,
        stream=False,
        think=True if model.startswith("deepseek") else False,
    )

    answer = Answer.model_validate_json(response.response.replace("\n", "").replace("{{", "{").replace("{\"{", "{"))
    return answer.answer if answer.isAnswered else None

if __name__ == "__main__":
    question = "What is the capital of france?"
    responses = [
        ("What is the capital of France?", "The capital of France is Paris."),
        ("Tell me about France.", "France is known for its rich history and culture."),
        ("What are some famous landmarks in Paris?", "Paris is also famous for its landmarks like the Eiffel Tower."),
        ("What color is the car?", "The car is red.")
    ]
    
    answer = response_answers_question(question, responses)
    print(answer)