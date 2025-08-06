'use client'

import { useState, useRef, useEffect } from 'react'
import axios from 'axios'

interface Message {
  id: string
  type: 'user' | 'assistant'
  content: string
  logs?: any[]
  timestamp: Date
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input.trim(),
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post('/api/logs/query', {
        query: userMessage.content,
        limit: 10
      })

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: response.data.answer,
        logs: response.data.relevant_logs,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error querying logs:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: 'Sorry, I encountered an error while processing your query.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-80px)]">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-20">
            <div className="text-4xl mb-4">💬</div>
            <p>Ask me anything about your logs...</p>
            <div className="mt-6 space-y-2 text-sm">
              <p className="text-gray-400">Try asking:</p>
              <div className="space-y-1">
                <p>"Show me all error logs"</p>
                <p>"What database issues occurred today?"</p>
                <p>"Find authentication failures"</p>
              </div>
            </div>
          </div>
        )}

        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-3xl ${message.type === 'user' ? 'bg-black text-white' : 'bg-gray-100'} rounded-lg p-4`}>
              <div className="whitespace-pre-wrap">{message.content}</div>
              
              {message.logs && message.logs.length > 0 && (
                <div className="mt-4 space-y-2">
                  <div className="text-sm font-medium text-gray-600">Relevant Logs:</div>
                  {message.logs.map((log, index) => (
                    <div key={index} className="bg-white border rounded p-3 text-sm">
                      <div className="flex justify-between items-center mb-1">
                        <span className="bg-gray-200 px-2 py-1 rounded text-xs">{log.service}</span>
                        <span className="text-gray-500 text-xs">{(log.score * 100).toFixed(1)}%</span>
                      </div>
                      <p className="text-gray-800">{log.message}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg p-4">
              <div className="flex items-center space-x-2">
                <div className="animate-pulse">Thinking...</div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t p-4">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
          <div className="flex space-x-4">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about your logs..."
              className="input flex-1"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="btn btn-primary h-10 px-6"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}