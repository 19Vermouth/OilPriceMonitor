"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertTriangle, TrendingUp, TrendingDown } from "lucide-react"

interface AnomalyCardProps {
  analytics: Record<string, any>
}

export function AnomalyCard({ analytics }: AnomalyCardProps) {
  const allAnomalies = Object.values(analytics).flatMap((a: any) => 
    (a.anomalies || []).map((an: any) => ({ ...an, crude: Object.keys(analytics).find(k => analytics[k] === a) }))
  )

  if (allAnomalies.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Anomaly Detection</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-3 text-green-500">
            <AlertTriangle className="h-5 w-5" />
            <span>No anomalies detected in recent data</span>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Anomaly Detection</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {allAnomalies.slice(0, 5).map((anomaly: any, i: number) => (
            <div
              key={i}
              className={`p-3 rounded-lg flex items-center justify-between ${
                anomaly.type === "spike" ? "bg-red-500/10" : "bg-orange-500/10"
              }`}
            >
              <div className="flex items-center gap-3">
                {anomaly.type === "spike" ? (
                  <TrendingUp className="h-5 w-5 text-red-500" />
                ) : (
                  <TrendingDown className="h-5 w-5 text-orange-500" />
                )}
                <div>
                  <p className="font-medium text-sm">
                    {anomaly.crude} - {anomaly.type === "spike" ? "Price Spike" : "Price Drop"}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    Z-Score: {anomaly.z_score} | Price: ${anomaly.price?.toFixed(2)}
                  </p>
                </div>
              </div>
              <span className={`text-sm font-medium ${anomaly.type === "spike" ? "text-red-500" : "text-orange-500"}`}>
                {anomaly.type === "spike" ? "+" : "-"}{anomaly.z_score}σ
              </span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
