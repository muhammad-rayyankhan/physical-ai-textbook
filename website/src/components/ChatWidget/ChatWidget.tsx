/**
 * ChatWidget Component
 *
 * Main container for the chat widget. Manages state and renders button/window.
 */

import React, { useState, useCallback } from 'react';
import ChatButton from './ChatButton';
import ChatWindow from './ChatWindow';
import { askQuestion, Message, AnswerResponse } from './chatApi';
import styles from './ChatWidget.module.css';

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);

  const handleToggle = useCallback(() => {
    setIsOpen((prev) => !prev);
    // Clear error when opening/closing
    setError(null);
  }, []);

  const handleSendMessage = useCallback(
    async (messageText: string) => {
      // Add user message
      const userMessage: Message = {
        id: `user-${Date.now()}`,
        type: 'user',
        content: messageText,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);
      setError(null);

      try {
        // Call API
        const response: AnswerResponse = await askQuestion(
          messageText,
          sessionId || undefined
        );

        // Store session ID
        if (!sessionId) {
          setSessionId(response.session_id);
        }

        // Add bot message
        const botMessage: Message = {
          id: `bot-${Date.now()}`,
          type: 'bot',
          content: response.answer,
          citations: response.citations,
          timestamp: new Date(),
        };

        setMessages((prev) => [...prev, botMessage]);
      } catch (err) {
        console.error('Error sending message:', err);
        const errorMessage =
          err instanceof Error
            ? err.message
            : 'Failed to get response. Please try again.';
        setError(errorMessage);

        // Add error message as bot response
        const errorBotMessage: Message = {
          id: `bot-error-${Date.now()}`,
          type: 'bot',
          content: `Sorry, I encountered an error: ${errorMessage}`,
          timestamp: new Date(),
        };

        setMessages((prev) => [...prev, errorBotMessage]);
      } finally {
        setIsLoading(false);
      }
    },
    [sessionId]
  );

  return (
    <div className={styles.chatWidget}>
      {isOpen && (
        <ChatWindow
          messages={messages}
          onSendMessage={handleSendMessage}
          onClose={handleToggle}
          isLoading={isLoading}
          error={error}
        />
      )}
      <ChatButton onClick={handleToggle} isOpen={isOpen} />
    </div>
  );
}
