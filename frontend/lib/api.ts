export interface ChatResponse {
  answer: string;
  sources: string[];
}

export class ApiError extends Error {}

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

/**
 * Sends a question to the RAG backend and returns the grounded answer
 * plus the source document names it was based on.
 */
export async function askQuestion(question: string): Promise<ChatResponse> {
  let response: Response;
  try {
    response = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: question }),
    });
  } catch {
    throw new ApiError(
      "Could not reach the chatbot API. Is the backend running and reachable?"
    );
  }

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const body = await response.json();
      detail = body.detail ?? detail;
    } catch {
      // ignore, fall back to statusText
    }
    throw new ApiError(`API error (${response.status}): ${detail}`);
  }

  return response.json();
}
