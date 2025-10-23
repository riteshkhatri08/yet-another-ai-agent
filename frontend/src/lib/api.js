// API helper for streaming chat responses.
// Expects backend to stream plain text chunks.

export async function streamChat(payload, onDelta) {
  const base = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
  const resp = await fetch(`${base}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`HTTP ${resp.status}: ${text}`);
  }

  if (!resp.body) {
    const data = await resp.text();
    onDelta(data);
    return;
  }

  const reader = resp.body.getReader();
  const decoder = new TextDecoder('utf-8');
  let buffer = '';
  while (true) {
    const { value, done } = await reader.read();
    if (value) {
      buffer += decoder.decode(value, { stream: !done });
      let lineBreakIndex;
      while ((lineBreakIndex = buffer.indexOf('\n')) >= 0) {
        const line = buffer.slice(0, lineBreakIndex).trim();
        buffer = buffer.slice(lineBreakIndex + 1);
        if (!line) continue;
        try {
          const obj = JSON.parse(line);
          if (obj.delta) {
            onDelta(obj.delta);
          } else if (obj.done) {
            return; // stream finished
          } else {
            // meta or other info ignored for now
          }
        } catch (e) {
          // Fallback: treat raw line as text
          onDelta(line);
        }
      }
    }
    if (done) break;
  }
}
