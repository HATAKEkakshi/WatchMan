'use client'

interface LogResult {
  id: string
  message: string
  service: string
  score: number
}

interface LogResultsProps {
  results: {
    answer: string
    relevant_logs: LogResult[]
  }
}

export default function LogResults({ results }: LogResultsProps) {
  if (!results) return null

  return (
    <div className="space-y-4">
      <div className="bg-blue-50 p-4 rounded-md">
        <h3 className="font-semibold text-blue-800 mb-2">AI Analysis</h3>
        <p className="text-blue-700 whitespace-pre-wrap">{results.answer}</p>
      </div>

      {results.relevant_logs && results.relevant_logs.length > 0 && (
        <div>
          <h3 className="font-semibold mb-3">Relevant Logs ({results.relevant_logs.length})</h3>
          <div className="space-y-2">
            {results.relevant_logs.map((log, index) => (
              <div key={log.id} className="border rounded-md p-3 bg-gray-50">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs bg-gray-200 px-2 py-1 rounded">
                    {log.service}
                  </span>
                  <span className="text-xs text-gray-500">
                    Score: {(log.score * 100).toFixed(1)}%
                  </span>
                </div>
                <p className="text-sm text-gray-800">{log.message}</p>
                <div className="text-xs text-gray-500 mt-1">ID: {log.id}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}