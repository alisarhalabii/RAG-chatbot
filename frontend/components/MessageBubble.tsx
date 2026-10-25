import ReactMarkdown from "react-markdown";
import type { ChatMessage } from "@/lib/types";

export default function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";
  const isError = message.role === "error";

  return (
    <div
      className={`flex w-full animate-fade-in ${isUser ? "justify-end" : "justify-start"}`}
    >
      <div
        className={`max-w-[85%] sm:max-w-[70%] rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-sm ${
          isUser
            ? "bg-brand-600 text-white rounded-br-sm"
            : isError
              ? "bg-red-50 text-red-700 border border-red-200 dark:bg-red-950/40 dark:text-red-300 dark:border-red-900 rounded-bl-sm"
              : "bg-white text-gray-800 border border-gray-200 dark:bg-gray-900 dark:text-gray-100 dark:border-gray-800 rounded-bl-sm"
        }`}
      >
        {isUser ? (
          <p className="whitespace-pre-wrap">{message.content}</p>
        ) : (
          <div className="prose-chat">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
        )}

        {message.sources && message.sources.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1.5 border-t border-gray-100 dark:border-gray-800 pt-2">
            {message.sources.map((source) => (
              <span
                key={source}
                className="rounded-full bg-brand-50 text-brand-700 dark:bg-brand-900/40 dark:text-brand-200 px-2 py-0.5 text-[11px] font-medium"
              >
                {source}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
