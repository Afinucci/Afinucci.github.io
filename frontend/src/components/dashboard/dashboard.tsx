'use client'

export function Dashboard() {
  return (
    <div className="space-y-4">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <StatsCard
          title="Total Products"
          value="1,234"
          change="+12%"
          changeType="positive"
        />
        <StatsCard
          title="Low Stock Items"
          value="23"
          change="+5"
          changeType="warning"
        />
        <StatsCard
          title="Total Value"
          value="€245,678"
          change="+8.2%"
          changeType="positive"
        />
      </div>

      <div className="rounded-lg border bg-card p-6">
        <h2 className="text-lg font-semibold mb-4">Recent Activity</h2>
        <div className="space-y-3">
          <ActivityItem
            action="Stock Updated"
            item="Product A"
            time="2 minutes ago"
          />
          <ActivityItem
            action="Order Created"
            item="Order #1234"
            time="15 minutes ago"
          />
          <ActivityItem
            action="Low Stock Alert"
            item="Product B"
            time="1 hour ago"
          />
        </div>
      </div>

      <div className="rounded-lg border bg-card p-6">
        <h2 className="text-lg font-semibold mb-4">AI Insights</h2>
        <div className="space-y-3 text-sm">
          <InsightItem
            icon="⚠️"
            message="Product A will run out in 2 days at current sales rate"
            action="Create Purchase Order"
          />
          <InsightItem
            icon="📈"
            message="Seasonal trend detected: Consider stocking for holidays"
            action="View Forecast"
          />
          <InsightItem
            icon="💰"
            message="Supplier Z increased prices by 15%. Alternative suppliers available"
            action="Compare Suppliers"
          />
        </div>
      </div>
    </div>
  )
}

function StatsCard({
  title,
  value,
  change,
  changeType,
}: {
  title: string
  value: string
  change: string
  changeType: 'positive' | 'negative' | 'warning'
}) {
  const changeColor =
    changeType === 'positive'
      ? 'text-green-600'
      : changeType === 'negative'
      ? 'text-red-600'
      : 'text-yellow-600'

  return (
    <div className="rounded-lg border bg-card p-6">
      <p className="text-sm font-medium text-muted-foreground">{title}</p>
      <div className="mt-2 flex items-baseline gap-2">
        <p className="text-2xl font-bold">{value}</p>
        <span className={`text-sm ${changeColor}`}>{change}</span>
      </div>
    </div>
  )
}

function ActivityItem({
  action,
  item,
  time,
}: {
  action: string
  item: string
  time: string
}) {
  return (
    <div className="flex items-center justify-between py-2 border-b last:border-0">
      <div>
        <p className="text-sm font-medium">{action}</p>
        <p className="text-xs text-muted-foreground">{item}</p>
      </div>
      <span className="text-xs text-muted-foreground">{time}</span>
    </div>
  )
}

function InsightItem({
  icon,
  message,
  action,
}: {
  icon: string
  message: string
  action: string
}) {
  return (
    <div className="flex items-start gap-3 rounded-md border p-3">
      <span className="text-xl">{icon}</span>
      <div className="flex-1">
        <p className="text-sm">{message}</p>
        <button className="mt-1 text-xs text-primary hover:underline">
          {action} →
        </button>
      </div>
    </div>
  )
}
