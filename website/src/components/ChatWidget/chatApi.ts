/**
 * Chat API Client
 *
 * Handles communication with the backend RAG chatbot API.
 */

const API_URL = 'http://localhost:8001';

export interface Citation {
  chapter_id: string;
  chapter_title: string;
  section: string;
  text_snippet?: string;
  relevance_score?: number;
}

export interface AnswerResponse {
  answer: string;
  citations: Citation[];
  sources: string[];
  session_id: string;
}

export interface Message {
  id: string;
  type: 'user' | 'bot';
  content: string;
  citations?: Citation[];
  timestamp: Date;
}

/**
 * Ask a question to the chatbot
 */
export async function askQuestion(
  message: string,
  sessionId?: string
): Promise<AnswerResponse> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

  try {
    const response = await fetch(`${API_URL}/api/chat/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        question: message,
        session_id: sessionId,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `Server error: ${response.status}`
      );
    }

    const data = await response.json();
    return data;
  } catch (error) {
    clearTimeout(timeoutId);

    if (error.name === 'AbortError') {
      throw new Error('Request timed out. Please try again.');
    }

    if (error instanceof TypeError && error.message === 'Failed to fetch') {
      throw new Error(
        'Unable to connect to the server. Please check if the backend is running.'
      );
    }

    throw error;
  }
}

/**
 * Get chat history for a session
 */
export async function getChatHistory(
  sessionId?: string,
  limit: number = 50
): Promise<any> {
  try {
    const params = new URLSearchParams();
    if (sessionId) params.append('session_id', sessionId);
    params.append('limit', limit.toString());

    const response = await fetch(
      `${API_URL}/api/chat/history?${params.toString()}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch chat history: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching chat history:', error);
    throw error;
  }
}

/**
 * Check API health
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/api/health`, {
      method: 'GET',
    });

    return response.ok;
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
}
