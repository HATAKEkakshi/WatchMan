import './globals.css'

export const metadata = {
  title: 'WatchMan - Log Intelligence',
  description: 'AI-powered log analysis and monitoring',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-white">
        {children}
      </body>
    </html>
  )
}