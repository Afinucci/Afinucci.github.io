import { ChatInterface } from '@/components/chat/chat-interface'
import { Dashboard } from '@/components/dashboard/dashboard'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col">
      <header className="border-b">
        <div className="container flex h-16 items-center justify-between py-4">
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold">WWS Inventory</h1>
            <span className="text-sm text-muted-foreground">AI-Powered</span>
          </div>
          <nav className="flex items-center gap-4">
            {/* Navigation items will go here */}
          </nav>
        </div>
      </header>

      <div className="flex-1 container grid gap-4 py-6 md:grid-cols-2 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <Dashboard />
        </div>
        <div className="lg:col-span-1">
          <ChatInterface />
        </div>
      </div>
    </main>
  )
}
