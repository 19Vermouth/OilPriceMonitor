"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { RiskScore, Alert } from "@/types"
import { AlertTriangle, Activity, Fuel, Globe } from "lucide-react"

interface DashboardStatsProps {
  prices: { WTI: number; BRENT: number; DUBAI: number; OPEC_BASKET: number }
  risk: RiskScore | null
  alerts: Alert[]
}

export function DashboardStats({ prices, risk, alerts }: DashboardStatsProps) {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium">WTI Crude</CardTitle>
          <Fuel className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            ${prices.WTI.toFixed(2)}
          </div>
          <p className="text-xs text-muted-foreground">per barrel</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium">Global Risk</CardTitle>
          <Globe className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            {risk?.global_score.toFixed(1) ?? "—"}
          </div>
          <Badge variant={risk?.level === "High" ? "high" : "secondary"}>
            {risk?.level ?? "Unknown"}
          </Badge>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium">Active Alerts</CardTitle>
          <AlertTriangle className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{alerts.length}</div>
          <p className="text-xs text-muted-foreground">
            {alerts.filter((a) => a.severity === "high").length} critical
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium">Data Sources</CardTitle>
          <Activity className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">2</div>
          <p className="text-xs text-muted-foreground">Connected</p>
        </CardContent>
      </Card>
    </div>
  )
}
