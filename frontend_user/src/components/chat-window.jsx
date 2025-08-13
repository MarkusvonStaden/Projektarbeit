import { Input, InputGroup } from "@/components/input";
import {
  MagnifyingGlassIcon,
  PaperAirplaneIcon,
} from "@heroicons/react/16/solid";
import { Button } from "@/components/button";
import { Message } from "@/components/message";
import { useState } from "react";

export function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [isSending, setIsSending] = useState(false);

  const handleSendMessage = async () => {
    if (inputText.trim()) {
      setIsSending(true);
      const userMessage = { text: inputText, role: "user" };
      setMessages([...messages, userMessage]);
      setInputText("");

      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
      const response = await fetch(`${backendUrl}/question`, {
        method: "POST",
        body: inputText,
      });

      const data = await response.json();
      const assistantMessage = {
        text: data.answer || "Waiting for Human",
        role: "assistant",
      };
      setMessages((prevMessages) => [...prevMessages, assistantMessage]);
    }
  };

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !isSending) {
      handleSendMessage();
    }
  };

  return (
    <div className="h-full w-full flex flex-col">
      <div className="flex-grow overflow-y-auto">
        {messages.map((msg, index) => (
          <Message
            key={index}
            text={msg.text}
            role={msg.role}
            isError={msg.error}
          />
        ))}
      </div>

      <div className="flex items-center space-x-2 p-2 -mb-4 h-20">
        <div className="flex-grow">
          <InputGroup>
            <MagnifyingGlassIcon className="text-gray-500" />
            <Input
              name="message"
              placeholder="Nachricht senden&hellip;"
              aria-label="Nachricht senden"
              value={inputText}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              disabled={isSending}
            />
          </InputGroup>
        </div>
        <Button
          color="blue"
          onClick={handleSendMessage}
          disabled={!inputText.trim() || isSending}
        >
          {isSending ? (
            <svg
              className="animate-spin h-5 w-5 text-white"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0c-3.14 0-6 1.39-8 4z"
              ></path>
            </svg>
          ) : (
            <PaperAirplaneIcon className="h-5 w-5" />
          )}
        </Button>
      </div>
    </div>
  );
}
