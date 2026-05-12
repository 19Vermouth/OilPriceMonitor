"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert } from "@/types"
import { AlertCircle } from "lucide-react"

interface AlertsListProps {
  alerts: Alert[]
}

const severityConfig: Record<string, { color: string; bg: string; icon: string }> = {
  high: { color: "text-red-500", bg: "bg-red-500/10", icon: "🔴" },
  medium: { color: "text-orange-500", bg: "bg-orange-500/10", icon: "🟡" },
  low: { color: "text-yellow-500", bg: "bg-yellow-500/10", icon: "🟢" },
}

export function AlertsList({ alerts }: AlertsListProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Active Alerts</CardTitle>
        <span className="text-2xl font-bold">{alerts.length}</span>
      </CardHeader>
      <CardContent>
        {alerts.length === 0 ? (
          <p className="text-muted-foreground text-sm">No active alerts</p>
        ) : (
          <div className="space-y-3">
            {alerts.map((alert) => {
              const config = severityConfig[alert.severity] || severityConfig.low
              return (
                <div
                  key={alert.id}
                  className={`flex items-start gap-3 p-3 rounded-lg ${config.bg}`}
                >
                  <AlertCircle className={`h-5 w-5 mt-0.5 ${config.color}`} />
                  <div className="flex-1">
                    <p className="text-sm font-medium">{alert.message}</p>
                    <p className="text-xs text-muted-foreground mt-1">
                      {alert.type.charAt(0).toUpperCase() + alert.type.slice(1)} Alert
                    </p>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
