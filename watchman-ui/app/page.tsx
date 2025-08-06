'use client'

import { useState } from 'react'
import LogForm from '../components/LogForm'
import ChatInterface from '../components/ChatInterface'

type Mode = 'select' | 'add' | 'query'

export default function Home() {
  const [mode, setMode] = useState<Mode>('select')

  if (mode === 'select') {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-8">
          <div>
            <h1 className="text-4xl font-bold mb-2">🕵️♂️ WatchMan</h1>
            <p className="text-gray-600">AI-powered log intelligence</p>
          </div>
          
          <div className="space-y-4">
            <button 
              onClick={() => setMode('add')}
              className="btn btn-primary h-12 px-8 w-full max-w-xs"
            >
              Add Logs
            </button>
            
            <button 
              onClick={() => setMode('query')}
              className="btn btn-secondary h-12 px-8 w-full max-w-xs"
            >
              Query Logs
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (mode === 'add') {
    return (
      <div className="min-h-screen">
        <header className="border-b p-4">
          <div className="flex items-center justify-between max-w-4xl mx-auto">
            <h1 className="text-xl font-semibold">Add Log Entry</h1>
            <button 
              onClick={() => setMode('select')}
              className="btn btn-secondary h-9 px-4"
            >
              Back
            </button>
          </div>
        </header>
        
        <main className="max-w-2xl mx-auto p-6">
          <div className="card">
            <LogForm onSuccess={() => setMode('select')} />
          </div>
        </main>
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      <header className="border-b p-4">
        <div className="flex items-center justify-between max-w-4xl mx-auto">
          <h1 className="text-xl font-semibold">Query Logs</h1>
          <button 
            onClick={() => setMode('select')}
            className="btn btn-secondary h-9 px-4"
          >
            Back
          </button>
        </div>
      </header>
      
      <main className="max-w-4xl mx-auto">
        <ChatInterface />
      </main>
    </div>
  )
}