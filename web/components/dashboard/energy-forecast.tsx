"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp, TrendingDown } from "lucide-react"

interface EnergyForecastCardProps {
  forecast: {
    region: string
    current: number
    forecast_1y: number
    growth_pct: number
  }[]
}

export function EnergyForecastCard({ forecast }: EnergyForecastCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Energy Demand Forecast</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {forecast.map((item) => {
            const isUp = item.growth_pct > 0
            return (
              <div key={item.region} className="p-3 rounded-lg bg-muted/50">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-sm">{item.region}</span>
                  <div className={`flex items-center gap-1 ${isUp ? "text-green-500" : "text-red-500"}`}>
                    {isUp ? (
                      <TrendingUp className="h-4 w-4" />
                    ) : (
                      <TrendingDown className="h-4 w-4" />
                    )}
                    <span className="text-sm font-medium">
                      {isUp ? "+" : ""}{item.growth_pct}%
                    </span>
                  </div>
                </div>
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>Current: {item.current.toLocaleString()} TWh</span>
                  <span>1Y Forecast: {item.forecast_1y.toLocaleString()} TWh</span>
                </div>
              </div>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}
