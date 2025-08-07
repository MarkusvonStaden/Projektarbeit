import { Strong, Text } from "@/components/text";
import { ThumbsDown, ThumbsUp } from "lucide-react";

export function UserMessage({ text }) {
  return (
    <div className="bg-blue-100 border border-blue-300 rounded-md p-4 mb-2">
      <Text className="text-blue-700">
        <Strong>Du:</Strong> {text}
      </Text>
    </div>
  );
}

export function AssistantMessage({ text, omit, markCorrect, isCorrect }) {
  return (
    <div className="bg-gray-100 border border-gray-300 rounded-md p-4 mb-2 flex flex-col">
      <div>
        <Text className="text-gray-700">
          <Strong>Assistent:</Strong> {text}
        </Text>
      </div>
      <div className="mt-2 flex items-center space-x-2">
        <button 
          className={`${isCorrect ? 'text-green-600' : 'text-gray-500 hover:text-green-500'}`}
          onClick={async () => {
            if (markCorrect) {
              await markCorrect();
            }
          }}
          disabled={isCorrect}
        >
          <ThumbsUp className="h-5 w-5" />
        </button>
        {isCorrect ? (
          <span className="text-gray-400 text-sm">
            Als korrekt markiert
          </span>
        ) : (
          <button
            className="text-gray-500 hover:text-red-500"
            onClick={async () => {
              if (omit) {
                await omit();
              }
            }}
          >
            <ThumbsDown className="h-5 w-5" />
          </button>
        )}
      </div>
    </div>
  );
}

export function InProgressMessage() {
  return (
    <div className="bg-orange-100 border border-orange-300 rounded-md p-4 mb-2">
      <Text className="text-orange-700">
        <Strong>System:</Strong> Ihre Anfrage wird bearbeitet...
      </Text>
    </div>
  );
}

export function OmittedMessage({ text }) {
  return (
    <div className="bg-red-100 border border-red-300 rounded-md p-4 mb-2">
      <Text className="text-red-700">
        <Strong>Abgelehnt:</Strong> {text}
      </Text>
    </div>
  );
}

export function Message({ role, text }) {
  if (role === "user") {
    return <UserMessage text={text} />;
  } else if (role === "assistant") {
    return <AssistantMessage text={text} />;
  }
  return null;
}
