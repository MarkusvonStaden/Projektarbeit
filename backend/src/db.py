from pymongo import MongoClient
import os
from bson import ObjectId

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB = os.getenv("MONGO_DB", "default_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "default_collection")

client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


def insert_question(question: str, answer: str| None = None) -> str:
    question = {
        "question": question,
        "answer": answer,
        "isAnswered": answer is not None,
        "omittedAnswers": [],
    }
    result = collection.insert_one(question)
    return str(result.inserted_id)


def get_question(question_id: str):
    if not ObjectId.is_valid(question_id):
        return None
    question_id = ObjectId(question_id)
    question = collection.find_one({"_id": question_id})
    if question:
        return {
            "id": str(question["_id"]),
            "question": question["question"],
            "answer": question.get("answer"),
            "isAnswered": question["isAnswered"],
            "omittedAnswers": question.get("omittedAnswers", []),
        }
    return None


def get_unanswered_questions():
    results = list(collection.find({"isAnswered": False}))
    return [
        {
            "id": str(question["_id"]),
            "question": question["question"]
        }
        for question in results
    ]


def insert_answer(question_id: str, answer: str):
    if not ObjectId.is_valid(question_id):
        return None
    question_id = ObjectId(question_id)
    result = collection.update_one(
        {"_id": question_id},
        {"$set": {"answer": answer, "isAnswered": True}}
    )
    return result.modified_count > 0


def get_all_questions():
    questions = collection.find()
    return [
        {
            "id": str(question["_id"]),
            "question": question["question"],
            "isAnswered": question["isAnswered"],
        }
        for question in questions
    ]