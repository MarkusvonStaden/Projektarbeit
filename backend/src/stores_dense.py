import os

from fastembed import TextEmbedding
from qdrant_client import QdrantClient, models
from uuid import uuid4

HOST = os.getenv("QDRANT_HOST", "localhost")
PORT = int(os.getenv("QDRANT_PORT", 6333))

client = QdrantClient(host=HOST, port=PORT)

dense_embedding_model = TextEmbedding("mixedbread-ai/mxbai-embed-large-v1")

if not client.collection_exists("q_and_a"):
    client.create_collection(
        collection_name="q_and_a",
        vectors_config={
            "questions": models.VectorParams(
                size=1024,
                distance=models.Distance.COSINE,
            ),
            "answers": models.VectorParams(
                size=1024,
                distance=models.Distance.COSINE,
            ),
        },
    )


def search(query: str):
    question_query_vector = next(dense_embedding_model.embed(query)).tolist()
    answer_query_vector = next(dense_embedding_model.query_embed(query)).tolist()

    filter = models.Filter(
        must_not=[
            models.IsEmptyCondition(
                is_empty=models.PayloadField(key="answer"),
            )
        ],
        must=[
            models.FieldCondition(key="isCorrect", match=models.MatchValue(value=True)),
        ]
    )

    prefetches = [
        models.Prefetch(
            query=question_query_vector, using="questions", limit=10, filter=filter
        ),
        models.Prefetch(
            query=answer_query_vector, using="answers", limit=10, filter=filter
        ),
    ]

    results = client.query_points(
        collection_name="q_and_a",
        prefetch=prefetches,
        query=models.FusionQuery(
            fusion=models.Fusion.RRF,
        ),
        limit=5,
        with_payload=True,
    )

    return [(point.payload.get("question"), point.payload.get("answer")) for point in results.points]


def get_all_questions():
    results = client.query_points(
        collection_name="q_and_a",
        limit=1000,
        with_payload=True,
    )

    return [
        {
            "id": point.id,
            "question": point.payload.get("question"),
            "answer": point.payload.get("answer"),
            "isCorrect": point.payload.get("isCorrect", False),
        }
        for point in results.points
    ]


def get_question_by_id(question_id: str):
    return client.retrieve(
        collection_name="q_and_a",
        ids=[question_id],
        with_payload=True,
    )[0].payload


def insert_question(question: str) -> str:
    question_vector = {
        "questions": next(dense_embedding_model.embed(question)).tolist()
    }

    id = str(uuid4())
    result = client.upsert(
        "q_and_a",
        points=[
            models.PointStruct(
                id=id,
                vector=question_vector,
                payload={
                    "question": question,
                    "answer": None,
                    "omittedAnswers": [],
                    "isCorrect": False,
                },
            )
        ],
    )
    print(result)
    return id


def insert_answer(question_id: str, answer: str):
    vector = {"answers": next(dense_embedding_model.embed(answer)).tolist()}

    result = client.set_payload(
        "q_and_a",
        points=[question_id],
        payload={
            "answer": answer,
            "isCorrect": False,
        },
    )
    if result.status == "completed":
        result = client.update_vectors(
            "q_and_a",
            points=[
                models.PointVectors(
                    id=question_id,
                    vector=vector,
                )
            ],
        )
    return result.status == "completed"


def omit_answer(question_id: str):
    current_payload = get_question_by_id(question_id)
    current_answer = current_payload.get("answer")
    omitted_answers = current_payload.get("omittedAnswers", [])

    omitted_answers.append(current_answer)
    updated_answer = ""

    payload_update = {
        "answer": updated_answer,
        "omittedAnswers": omitted_answers,
        "isCorrect": False,
    }

    result = client.set_payload(
        "q_and_a",
        points=[question_id],
        payload=payload_update,
    )

    if result.status == "completed":
        result = client.delete_vectors(
            collection_name="q_and_a", points=[question_id], vectors=["answers"]
        )
    return get_question_by_id(question_id)


def mark_answer_correct(question_id: str):
    payload_update = {
        "isCorrect": True,
    }

    result = client.set_payload(
        "q_and_a",
        points=[question_id],
        payload=payload_update,
    )

    return get_question_by_id(question_id) if result.status == "completed" else None
