# Yet Another AI Agent Frontend

Simple React + Vite chat UI that streams responses from a backend at `VITE_API_BASE_URL`.

## Setup

Copy `.env.example` to `.env` and adjust:
```
VITE_API_BASE_URL=http://localhost:8000
```

Install dependencies and run dev server:
```
npm install
npm run dev
```

Build production:
```
npm run build
```

Preview build:
```
npm run preview
```

## Streaming
The `streamChat` helper performs a POST to `/chat` and reads the ReadableStream to update UI as chunks arrive.

## Folder Structure
- `src/App.jsx` root component
- `src/components/Chat.jsx` chat UI
- `src/lib/api.js` streaming fetch helper
- `src/styles.css` minimal styles

## Tests
Add Vitest tests in `src/__tests__`. Example not included yet.

## Future Enhancements
- Authentication handling
- Message persistence
- Improved error handling & retries
- SSE or WebSocket support
