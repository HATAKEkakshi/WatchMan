'use client'

import { useState } from 'react'
import axios from 'axios'

interface LogFormProps {
  onSuccess?: () => void
}

export default function LogForm({ onSuccess }: LogFormProps) {
  const [formData, setFormData] = useState({
    service: 'backend',
    level: 'INFO',
    message: '',
    metadata: ''
  })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      await axios.post('/api/logs/', {
        level: formData.level,
        message: formData.message,
        metadata: formData.metadata || null
      }, {
        headers: {
          'service': formData.service,
          'Content-Type': 'application/json'
        }
      })
      
      setFormData({ ...formData, message: '', metadata: '' })
      onSuccess?.()
    } catch (error) {
      console.error('Error creating log:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-2">Service</label>
          <select 
            value={formData.service}
            onChange={(e) => setFormData({ ...formData, service: e.target.value })}
            className="input"
          >
            <option value="backend">Backend</option>
            <option value="auth">Auth</option>
            <option value="frontend">Frontend</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Level</label>
          <select 
            value={formData.level}
            onChange={(e) => setFormData({ ...formData, level: e.target.value })}
            className="input"
          >
            <option value="INFO">INFO</option>
            <option value="WARN">WARN</option>
            <option value="ERROR">ERROR</option>
            <option value="DEBUG">DEBUG</option>
          </select>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Message</label>
        <textarea 
          value={formData.message}
          onChange={(e) => setFormData({ ...formData, message: e.target.value })}
          className="textarea min-h-[120px]"
          placeholder="Enter log message..."
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Metadata</label>
        <input 
          type="text"
          value={formData.metadata}
          onChange={(e) => setFormData({ ...formData, metadata: e.target.value })}
          className="input"
          placeholder="Optional metadata..."
        />
      </div>

      <button 
        type="submit" 
        disabled={loading}
        className="btn btn-primary h-11 px-6 w-full"
      >
        {loading ? 'Creating...' : 'Create Log'}
      </button>
    </form>
  )
}