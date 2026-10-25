"use client";

import { useEffect, useRef, useState } from "react";
import MessageBubble from "@/components/MessageBubble";
import ChatInput from "@/components/ChatInput";
import TypingIndicator from "@/components/TypingIndicator";
import ThemeToggle from "@/components/ThemeToggle";
import { askQuestion, ApiError } from "@/lib/api";
import type { ChatMessage } from "@/lib/types";

const SUGGESTIONS = [
  "Hva handler dette datasettet om?",
  "Kan du oppsummere hovedpoengene?",
  "Hva er RAG?",
];

function newId() {
  return Math.random().toString(36).slice(2);
}

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  async function handleSend(text: string) {
    const userMessage: ChatMessage = { id: newId(), role: "user", content: text };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const { answer, sources } = await askQuestion(text);
      setMessages((prev) => [
        ...prev,
        { id: newId(), role: "assistant", content: answer, sources },
      ]);
    } catch (err) {
      const message =
        err instanceof ApiError ? err.message : "Noe gikk galt. Prøv igjen.";
      setMessages((prev) => [...prev, { id: newId(), role: "error", content: message }]);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="mx-auto flex h-screen max-w-3xl flex-col px-4">
      <header className="flex items-center justify-between border-b border-gray-200 py-4 dark:border-gray-800">
        <div>
          <h1 className="text-lg font-semibold tracking-tight">RAG Chatbot</h1>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Svar basert på et eget dokumentbibliotek
          </p>
        </div>
        <ThemeToggle />
      </header>

      <main className="chat-scroll flex-1 space-y-4 overflow-y-auto py-6">
        {messages.length === 0 && (
          <div className="flex h-full flex-col items-center justify-center gap-4 text-center">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-brand-100 text-brand-700 dark:bg-brand-900/40 dark:text-brand-300">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="h-6 w-6">
                <path
                  fillRule="evenodd"
                  d="M4.848 2.771A49.144 49.144 0 0 1 12 2.25c2.43 0 4.817.178 7.152.52 1.978.292 3.348 2.024 3.348 3.97v6.02c0 1.946-1.37 3.678-3.348 3.97a48.901 48.901 0 0 1-3.476.383.39.39 0 0 0-.297.17l-2.755 4.133a.75.75 0 0 1-1.248 0l-2.755-4.133a.39.39 0 0 0-.297-.17 48.9 48.9 0 0 1-3.476-.384c-1.978-.29-3.348-2.023-3.348-3.97V6.741c0-1.946 1.37-3.677 3.348-3.97Z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div>
              <p className="font-medium text-gray-800 dark:text-gray-100">
                Still et spørsmål om dokumentene dine
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Svarene er hentet fra det som er lastet inn i kunnskapsbasen
              </p>
            </div>
            <div className="flex flex-wrap justify-center gap-2">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  onClick={() => handleSend(s)}
                  className="rounded-full border border-gray-200 px-3 py-1.5 text-xs text-gray-600 transition-colors hover:border-brand-300 hover:text-brand-700 dark:border-gray-700 dark:text-gray-300 dark:hover:border-brand-700 dark:hover:text-brand-300"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="rounded-2xl rounded-bl-sm border border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-900">
              <TypingIndicator />
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </main>

      <footer className="border-t border-gray-200 py-4 dark:border-gray-800">
        <ChatInput onSend={handleSend} disabled={isLoading} />
        <p className="mt-2 text-center text-[11px] text-gray-400 dark:text-gray-600">
          Svar kan inneholde feil — sjekk kildene under hvert svar.
        </p>
      </footer>
    </div>
  );
}
