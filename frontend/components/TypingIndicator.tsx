export default function TypingIndicator() {
  return (
    <div className="flex items-center gap-1 px-4 py-3">
      <span className="h-2 w-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-blink [animation-delay:-0.2s]" />
      <span className="h-2 w-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-blink [animation-delay:-0.1s]" />
      <span className="h-2 w-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-blink" />
    </div>
  );
}
