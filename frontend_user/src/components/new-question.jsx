import React, { useState } from "react";
import { Input } from "@/components/input";
import { PaperAirplaneIcon } from "@heroicons/react/24/solid";
import { useNavigate } from "react-router-dom";

export function NewQuestion( { updateSidebar }) {
  const navigate = useNavigate();
  const [inputValue, setInputValue] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!inputValue.trim()) return;
    setInputValue("");

    const response = await fetch("http://localhost/questions", {
      method: "POST",
      body: inputValue,
    });

    const data = await response.json();
    updateSidebar();
    navigate(`/user/${data.id}`);
  };

  return (
    <div
      className="flex h-full w-full flex-col dark:bg-zinc-900 
                    justify-between md:justify-center md:items-center"
    >
      <div className="w-full max-w-2xl px-4 mt-8 md:mt-0 md:mb-8">
        <h1 className="text-center text-4xl font-bold tracking-tight text-zinc-900 dark:text-white sm:text-5xl">
          Wie kann ich dir helfen?
        </h1>
      </div>

      <div className="w-full px-4 pb-4 sm:pb-6 md:pb-0">
        <form
          onSubmit={handleSubmit}
          className="mx-auto flex w-full max-w-2xl items-start gap-x-3"
        >
          <div className="flex gap-2 w-full">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Stelle deine Frage..."
              className="flex-1 p-3 border border-zinc-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-zinc-700 dark:border-zinc-600 dark:text-white"
            />
          </div>
          <button
            type="submit"
            className="p-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            <PaperAirplaneIcon className="h-5 w-5" />
          </button>
        </form>
      </div>
    </div>
  );
}
