import React, { useState, useRef, useEffect } from 'react';
import { streamChat } from '../lib/api.js';

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const scrollRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  async function handleSend(e) {
    e.preventDefault();
    if (!input.trim()) return;
    const userMsg = { role: 'user', content: input };
    setMessages(m => [...m, userMsg]);
    setInput('');
    // Immediately refocus input so user can continue typing while model streams
    if (inputRef.current) {
      // Use requestAnimationFrame to ensure React state update cycle doesn't steal focus
      requestAnimationFrame(() => inputRef.current?.focus());
    }
    setLoading(true);
    setError(null);

    try {
      let assistantContent = '';
      await streamChat({ message: userMsg.content }, (delta) => {
        assistantContent += delta;
        setMessages(m => {
          const copy = [...m];
          if (copy[copy.length - 1]?.role === 'assistant-stream') {
            copy[copy.length - 1].content = assistantContent;
          } else {
            copy.push({ role: 'assistant-stream', content: assistantContent });
          }
          return copy;
        });
      });

      // finalize assistant message
      setMessages(m => m.map(msg => msg.role === 'assistant-stream' ? { role: 'assistant', content: msg.content } : msg));
    } catch (err) {
      console.error(err);
      setError(err.message || 'Failed to get response');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="chat">
      <div className="chat__messages" ref={scrollRef}>
        {messages.map((m, i) => (
          <div key={i} className={`msg msg--${m.role}`}>{m.content}</div>
        ))}
        {loading && <div className="msg msg--system">Model thinking...</div>}
        {error && <div className="msg msg--error">{error}</div>}
      </div>
      <form className="chat__form" onSubmit={handleSend}>
        <input
          ref={inputRef}
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your message"
          // Keep enabled to preserve focus; rely on button disable to prevent duplicate sends
        />
        <button type="submit" disabled={loading || !input.trim()} className="btn btn--primary">Send</button>
      </form>
    </div>
  );
}
