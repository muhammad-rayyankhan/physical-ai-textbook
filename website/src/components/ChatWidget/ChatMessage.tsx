/**
 * ChatMessage Component
 *
 * Renders a single message bubble (user or bot) with citations.
 */

import React from 'react';
import { Message, Citation } from './chatApi';
import styles from './ChatWidget.module.css';

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.type === 'user';

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
    });
  };

  const renderCitations = (citations: Citation[]) => {
    if (!citations || citations.length === 0) return null;

    return (
      <div className={styles.citations}>
        <div className={styles.citationsLabel}>Sources:</div>
        {citations.map((citation, index) => (
          <a
            key={index}
            href={`/docs/${citation.chapter_id}`}
            className={styles.citationLink}
            target="_blank"
            rel="noopener noreferrer"
          >
            {citation.chapter_title} - {citation.section}
          </a>
        ))}
      </div>
    );
  };

  return (
    <div
      className={`${styles.messageContainer} ${
        isUser ? styles.userMessage : styles.botMessage
      }`}
    >
      <div className={styles.messageBubble}>
        <div className={styles.messageContent}>{message.content}</div>
        {!isUser && message.citations && renderCitations(message.citations)}
        <div className={styles.messageTime}>{formatTime(message.timestamp)}</div>
      </div>
    </div>
  );
}
