/**
 * Root Component
 *
 * Wraps the entire Docusaurus app to render ChatWidget on all pages.
 */

import React from 'react';
import ChatWidget from '@site/src/components/ChatWidget/ChatWidget';

export default function Root({ children }) {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}
