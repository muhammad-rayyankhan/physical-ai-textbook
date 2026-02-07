/**
 * ChatWindow Component
 *
 * Main chat interface with header, message list, and input field.
 */

import React, { useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { Message } from './chatApi';
import styles from './ChatWidget.module.css';

interface ChatWindowProps {
  messages: Message[];
  onSendMessage: (message: string) => void;
  onClose: () => void;
  isLoading: boolean;
  error: string | null;
}

export default function ChatWindow({
  messages,
  onSendMessage,
  onClose,
  isLoading,
  error,
}: ChatWindowProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className={styles.chatWindow}>
      {/* Header */}
      <div className={styles.chatHeader}>
        <div className={styles.headerContent}>
          <h3 className={styles.headerTitle}>Ask about Physical AI</h3>
          <p className={styles.headerSubtitle}>
            Questions about the textbook content
          </p>
        </div>
        <button
          onClick={onClose}
          className={styles.closeButton}
          aria-label="Close chat"
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>

      {/* Messages */}
      <div className={styles.messagesContainer}>
        {messages.length === 0 ? (
          <div className={styles.emptyState}>
            <div className={styles.emptyIcon}>💬</div>
            <h4>Start a conversation</h4>
            <p>Ask me anything about Physical AI and Humanoid Robotics!</p>
            <div className={styles.suggestedQuestions}>
              <button
                onClick={() => onSendMessage('What is Physical AI?')}
                className={styles.suggestedQuestion}
              >
                What is Physical AI?
              </button>
              <button
                onClick={() => onSendMessage('How do sensors work in robots?')}
                className={styles.suggestedQuestion}
              >
                How do sensors work?
              </button>
              <button
                onClick={() => onSendMessage('Explain PID control')}
                className={styles.suggestedQuestion}
              >
                Explain PID control
              </button>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            {isLoading && (
              <div className={styles.loadingIndicator}>
                <div className={styles.loadingDots}>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <span>Thinking...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Error message */}
      {error && (
        <div className={styles.errorMessage}>
          <span className={styles.errorIcon}>⚠️</span>
          {error}
        </div>
      )}

      {/* Input */}
      <ChatInput onSend={onSendMessage} disabled={isLoading} />
    </div>
  );
}
