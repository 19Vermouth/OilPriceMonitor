"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ScatterChart, Scatter, XAxis, YAxis, ZAxis, Tooltip, ResponsiveContainer, ReferenceLine } from "recharts"

interface RiskTrendProps {
  trends: {
    date: string
    score: number
    level: string
  }[]
}

export function RiskTrendChart({ trends }: RiskTrendProps) {
  const chartData = trends.map((t) => ({
    date: new Date(t.date).getTime(),
    score: t.score,
    level: t.level,
    label: new Date(t.date).toLocaleDateString("en-US", { month: "short", day: "numeric" }),
  }))

  return (
    <Card>
      <CardHeader>
        <CardTitle>Risk Score Over Time (30 Days)</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
            <XAxis
              type="number"
              dataKey="date"
              domain={["auto", "auto"]}
              tickFormatter={(v) => new Date(v).toLocaleDateString("en-US", { month: "short", day: "numeric" })}
              tick={{ fontSize: 11 }}
            />
            <YAxis
              type="number"
              dataKey="score"
              domain={[0, 100]}
              tick={{ fontSize: 11 }}
              tickFormatter={(v) => `${v}`}
            />
            <ZAxis range={[60, 60]} />
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const data = payload[0].payload
                  return (
                    <div className="bg-white dark:bg-slate-900 p-2 rounded border shadow-lg">
                      <p className="font-medium">{data.label}</p>
                      <p className="text-sm text-gray-600">Risk: {data.score.toFixed(1)}</p>
                      <p className="text-sm text-gray-600">Level: {data.level}</p>
                    </div>
                  )
                }
                return null
              }}
            />
            <ReferenceLine y={70} stroke="#ef4444" strokeDasharray="3 3" label={{ value: "Critical", fill: "#ef4444", fontSize: 10 }} />
            <ReferenceLine y={50} stroke="#eab308" strokeDasharray="3 3" label={{ value: "High", fill: "#eab308", fontSize: 10 }} />
            <Scatter
              data={chartData}
              fill="#8b5cf6"
              shape="circle"
            />
          </ScatterChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
