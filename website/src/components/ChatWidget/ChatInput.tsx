/**
 * ChatInput Component
 *
 * Text input field with send button for user messages.
 */

import React, { useState, KeyboardEvent, ChangeEvent } from 'react';
import styles from './ChatWidget.module.css';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export default function ChatInput({
  onSend,
  disabled = false,
  placeholder = 'Ask a question about the textbook...',
}: ChatInputProps) {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    const trimmedMessage = message.trim();
    if (trimmedMessage && !disabled) {
      onSend(trimmedMessage);
      setMessage('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Send on Enter, new line on Shift+Enter
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    // Limit to 500 characters
    if (value.length <= 500) {
      setMessage(value);
    }
  };

  const isValid = message.trim().length >= 3;

  return (
    <div className={styles.chatInput}>
      <textarea
        value={message}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={disabled}
        className={styles.inputField}
        rows={2}
        aria-label="Message input"
      />
      <div className={styles.inputFooter}>
        <span className={styles.charCounter}>
          {message.length}/500
        </span>
        <button
          onClick={handleSend}
          disabled={disabled || !isValid}
          className={styles.sendButton}
          aria-label="Send message"
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
            <line x1="22" y1="2" x2="11" y2="13" />
            <polygon points="22 2 15 22 11 13 2 9 22 2" />
          </svg>
        </button>
      </div>
    </div>
  );
}
