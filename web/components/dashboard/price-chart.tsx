"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts"

interface PriceChartProps {
  prices: { WTI: number; BRENT: number; DUBAI: number; OPEC_BASKET: number }
}

const COLORS = {
  WTI: "#3b82f6",
  BRENT: "#10b981",
  DUBAI: "#f59e0b",
  OPEC_BASKET: "#8b5cf6",
}

function generateHistoricalData(currentPrices: PriceChartProps["prices"]) {
  const data = []
  for (let i = 7; i >= 0; i--) {
    const date = new Date()
    date.setDate(date.getDate() - i)
    data.push({
      date: date.toLocaleDateString("en-US", { month: "short", day: "numeric" }),
      WTI: (currentPrices.WTI || 78) + (Math.random() - 0.5) * 4,
      BRENT: (currentPrices.BRENT || 82) + (Math.random() - 0.5) * 4,
      DUBAI: (currentPrices.DUBAI || 80) + (Math.random() - 0.5) * 4,
      OPEC_BASKET: (currentPrices.OPEC_BASKET || 79) + (Math.random() - 0.5) * 4,
    })
  }
  return data
}

export function PriceChart({ prices }: PriceChartProps) {
  const chartData = generateHistoricalData(prices)

  const crudeTypes = [
    { key: "WTI", label: "WTI" },
    { key: "BRENT", label: "Brent" },
    { key: "DUBAI", label: "Dubai" },
    { key: "OPEC_BASKET", label: "OPEC Basket" },
  ]

  return (
    <Card className="col-span-2">
      <CardHeader>
        <CardTitle>Crude Oil Prices (USD/barrel) - 7 Day Trend</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          {crudeTypes.map((c) => (
            <div key={c.key} className="p-3 rounded-lg bg-muted/50">
              <p className="text-sm text-muted-foreground">{c.label}</p>
              <p className="text-2xl font-bold" style={{ color: COLORS[c.key as keyof typeof COLORS] }}>
                ${(prices[c.key as keyof typeof prices] || 0).toFixed(2)}
              </p>
            </div>
          ))}
        </div>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <XAxis dataKey="date" />
            <YAxis domain={["auto", "auto"]} tickFormatter={(v) => `$${v}`} />
            <Tooltip
              formatter={(value) => [`$${Number(value).toFixed(2)}`]}
              contentStyle={{
                backgroundColor: "var(--color-card)",
                border: "1px solid var(--color-border)",
                borderRadius: "0.5rem",
              }}
            />
            <Legend />
            {crudeTypes.map((c) => (
              <Line
                key={c.key}
                type="monotone"
                dataKey={c.key}
                stroke={COLORS[c.key as keyof typeof COLORS]}
                strokeWidth={2}
                dot={{ fill: COLORS[c.key as keyof typeof COLORS], strokeWidth: 2, r: 3 }}
                name={c.label}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
