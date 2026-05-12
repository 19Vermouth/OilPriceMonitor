"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp, TrendingDown, Minus } from "lucide-react"

interface PriceAnalyticsProps {
  analytics: Record<string, any>
}

const COLORS: Record<string, string> = {
  WTI: "#3b82f6",
  BRENT: "#10b981",
  DUBAI: "#f59e0b",
  OPEC_BASKET: "#8b5cf6",
}

export function PriceAnalyticsCard({ analytics }: PriceAnalyticsProps) {
  const crudeTypes = ["WTI", "BRENT", "DUBAI", "OPEC_BASKET"]

  return (
    <Card className="col-span-2">
      <CardHeader>
        <CardTitle>Price Analytics</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {crudeTypes.map((crude) => {
            const data = analytics[crude] || {}
            const change = data.change_daily || 0
            const isUp = change > 0
            const isNeutral = change === 0

            return (
              <div key={crude} className="p-4 rounded-lg bg-muted/50">
                <div className="flex items-center justify-between mb-3">
                  <span className="font-semibold" style={{ color: COLORS[crude] }}>
                    {crude}
                  </span>
                  <div className="flex items-center gap-2">
                    {isNeutral ? (
                      <Minus className="h-4 w-4 text-gray-400" />
                    ) : isUp ? (
                      <TrendingUp className="h-4 w-4 text-green-500" />
                    ) : (
                      <TrendingDown className="h-4 w-4 text-red-500" />
                    )}
                    <span className={isUp ? "text-green-500" : isNeutral ? "text-gray-400" : "text-red-500"}>
                      {isUp ? "+" : ""}{change.toFixed(2)}%
                    </span>
                  </div>
                </div>
                <div className="grid grid-cols-4 gap-4 text-sm">
                  <div>
                    <p className="text-muted-foreground">Current</p>
                    <p className="font-medium">${data.current?.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">MA 7D</p>
                    <p className="font-medium">${data.ma_7?.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">Volatility</p>
                    <p className="font-medium">{data.volatility?.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">Weekly</p>
                    <p className={`font-medium ${data.change_weekly > 0 ? "text-green-500" : "text-red-500"}`}>
                      {data.change_weekly > 0 ? "+" : ""}{data.change_weekly?.toFixed(2)}%
                    </p>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}
