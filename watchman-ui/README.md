# WatchMan UI

Next.js frontend for WatchMan Log Intelligence API.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Open http://localhost:3000

## Features

- **Create Logs**: Add new log entries with service headers
- **Query Logs**: AI-powered semantic search through logs
- **Real-time Results**: View AI analysis and relevant log matches
- **Service Filtering**: Filter logs by service (backend/auth/frontend)

## API Integration

The UI connects to the FastAPI backend running on http://localhost:8000 via Next.js API proxy.