'use client'

import { useState } from 'react'
import axios from 'axios'

interface QueryFormProps {
  onResults: (results: any) => void
  loading: boolean
  setLoading: (loading: boolean) => void
}

export default function QueryForm({ onResults, loading, setLoading }: QueryFormProps) {
  const [query, setQuery] = useState('')
  const [service, setService] = useState('')
  const [limit, setLimit] = useState(10)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    try {
      const response = await axios.post('/api/logs/query', {
        query: query.trim(),
        service: service || null,
        limit
      })
      
      onResults(response.data)
    } catch (error) {
      console.error('Error querying logs:', error)
      onResults(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-1">Query</label>
        <textarea 
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full p-2 border rounded-md h-20"
          placeholder="Ask about your logs... (e.g., 'Show me all database errors')"
          required
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">Service (optional)</label>
          <select 
            value={service}
            onChange={(e) => setService(e.target.value)}
            className="w-full p-2 border rounded-md"
          >
            <option value="">All Services</option>
            <option value="backend">Backend</option>
            <option value="auth">Auth</option>
            <option value="frontend">Frontend</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Limit</label>
          <input 
            type="number"
            value={limit}
            onChange={(e) => setLimit(parseInt(e.target.value))}
            className="w-full p-2 border rounded-md"
            min="1"
            max="50"
          />
        </div>
      </div>

      <button 
        type="submit" 
        disabled={loading || !query.trim()}
        className="w-full bg-green-600 text-white p-2 rounded-md hover:bg-green-700 disabled:opacity-50"
      >
        {loading ? 'Searching...' : 'Query Logs'}
      </button>
    </form>
  )
}