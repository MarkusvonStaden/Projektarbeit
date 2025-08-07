import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { PaperAirplaneIcon } from '@heroicons/react/24/solid';
import {
  UserMessage,
  AssistantMessage,
  InProgressMessage,
  OmittedMessage,
} from '@/components/message';


const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

async function fetchQuestion(id) {
  try {
    const response = await fetch(`${API_BASE_URL}/questions/${id}`);
    if (!response.ok) {
      throw new Error(`Network response was not ok: ${response.statusText}`);
    }
    return await response.json();
  } catch (err) {
    console.error("Failed to fetch question:", err);
    return null;
  }
}

async function postOmitAnswer(id) {
  try {
    const response = await fetch(`${API_BASE_URL}/questions/${id}/omit`, { method: 'POST' });
    if (!response.ok) {
      throw new Error(`Network response was not ok: ${response.statusText}`);
    }
    return await response.json();
  } catch (err) {
    console.error("Failed to omit answer:", err);
    return null;
  }
}

async function postMarkCorrect(id) {
  try {
    const response = await fetch(`${API_BASE_URL}/questions/${id}/correct`, { method: 'POST' });
    if (!response.ok) {
      throw new Error(`Network response was not ok: ${response.statusText}`);
    }
    return await response.json();
  } catch (err) {
    console.error("Failed to mark answer as correct:", err);
    return null;
  }
}

async function postAnswer(id, answer) {
  try {
    const response = await fetch(`${API_BASE_URL}/questions/${id}/answer`, {
      method: 'POST',
      body: answer,
    });
    if (!response.ok) {
      throw new Error(`Network response was not ok: ${response.statusText}`);
    }
    return await response.json();
  } catch (err) {
    console.error("Failed to post answer:", err);
    return null;
  }
}


function useQuestion(id) {
  const [question, setQuestion] = useState(null);

  useEffect(() => {
    if (id) {
      fetchQuestion(id).then(setQuestion);
    }
  }, [id]);

  return { question, setQuestion };
}


function QuestionDisplay({ question }) {
  if (!question) {
    return <p>Loading...</p>;
  }

  return (
    <>
      <UserMessage text={question.question} />
      {question.omittedAnswers?.length > 0 && (
        <div className="mt-4">
          {question.omittedAnswers.map((msg, i) => (
            <OmittedMessage key={i} text={msg} />
          ))}
        </div>
      )}
    </>
  );
}


export function UserView({ updateSidebar }) {
  const { id } = useParams();
  const { question, setQuestion } = useQuestion(id);

  const handleOmitAnswer = async () => {
    const updatedQuestion = await postOmitAnswer(id);
    if (updatedQuestion) {
      setQuestion(updatedQuestion);
    }
    updateSidebar();
  };

  const handleMarkCorrect = async () => {
    const updatedQuestion = await postMarkCorrect(id);
    if (updatedQuestion) {
      setQuestion(updatedQuestion);
    }
    updateSidebar();
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 p-6 lg:rounded-lg lg:bg-red lg:p-10 lg:shadow-xs lg:ring-1 lg:ring-zinc-950/5 dark:lg:bg-zinc-900 dark:lg:ring-white/10">
        <div className="mx-auto max-w-6xl h-full flex flex-col justify-center">
          <QuestionDisplay question={question} />
          {question && (
            question.answer ? (
              <AssistantMessage 
                text={question.answer} 
                omit={handleOmitAnswer} 
                markCorrect={handleMarkCorrect} 
                isCorrect={question.isCorrect}
              />
            ) : (
              <InProgressMessage />
            )
          )}
        </div>
      </div>
    </div>
  );
}

export function AdminView({ updateSidebar }) {
  const { id } = useParams();
  const { question } = useQuestion(id);
  const [inputMessage, setInputMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    await postAnswer(id, inputMessage);
    
    setInputMessage('');
    updateSidebar();
    navigate(`/user/${id}`);
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 p-6 lg:rounded-lg lg:bg-red lg:p-10 lg:shadow-xs lg:ring-1 lg:ring-zinc-950/5 dark:lg:bg-zinc-900 dark:lg:ring-white/10">
        <div className="mx-auto max-w-6xl h-full flex flex-col justify-center">
          <QuestionDisplay question={question} />
        </div>
      </div>

      <div className="sticky bottom-0 bg-white dark:bg-zinc-800 p-4">
        <div className="mx-auto max-w-6xl">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Deine Nachricht hier..."
              className="flex-1 p-3 border border-zinc-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-zinc-700 dark:border-zinc-600 dark:text-white"
            />
            <button
              type="submit"
              className="p-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              <PaperAirplaneIcon className="h-5 w-5" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}