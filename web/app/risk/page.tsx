"use client"

import { useState, useEffect, useCallback } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { RiskTrendChart } from "@/components/dashboard/risk-scatter"
import { RiskDisplay } from "@/components/dashboard/risk-display"
import { RefreshButton } from "@/components/dashboard/refresh-button"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export default function RiskPage() {
  const [riskData, setRiskData] = useState<any>(null)
  const [trends, setTrends] = useState<any[]>([])
  const [regions, setRegions] = useState<Record<string, number>>({})
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)
  const [loading, setLoading] = useState(true)

  const loadData = useCallback(async () => {
    try {
      const [riskRes, trendsRes, heatmapRes] = await Promise.all([
        fetch(`${API_URL}/api/v1/risk/global`).then(r => r.json()),
        fetch(`${API_URL}/api/v1/analytics/risk/trend`).then(r => r.json()),
        fetch(`${API_URL}/api/v1/risk/heatmap`).then(r => r.json()),
      ])
      
      setRiskData(riskRes)
      setTrends(trendsRes.trends || [])
      setRegions(heatmapRes.regions || {})
      setLastUpdated(new Date())
    } catch (error) {
      console.error("Failed to fetch data:", error)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadData()
  }, [loadData])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Risk Analysis</h1>
          <p className="text-muted-foreground">Geopolitical risk monitoring and trends</p>
        </div>
        <RefreshButton onRefresh={loadData} lastUpdated={lastUpdated} />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <RiskDisplay risk={riskData || { global_score: 0, level: "Unknown", factors: [], region: null }} />
        <Card>
          <CardHeader>
            <CardTitle>Risk Factors</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {(riskData?.factors || []).map((factor: string, i: number) => (
                <div key={i} className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-orange-500" />
                  <span className="text-sm">{factor}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      <RiskTrendChart trends={trends} />

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Risk by Region</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {Object.entries(regions).map(([region, score]) => (
                <div key={region} className="flex items-center justify-between">
                  <span className="text-sm font-medium">{region.replace("_", " ")}</span>
                  <div className="flex items-center gap-2">
                    <div className="w-32 h-2 bg-muted rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full"
                        style={{
                          width: `${score}%`,
                          backgroundColor: score >= 70 ? "#ef4444" : score >= 50 ? "#eab308" : "#22c55e",
                        }}
                      />
                    </div>
                    <span className="text-sm font-medium w-8">{score}</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Risk Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { label: "Critical (70+)", count: Object.values(regions).filter((s: number) => s >= 70).length, color: "#ef4444" },
                { label: "High (50-69)", count: Object.values(regions).filter((s: number) => s >= 50 && s < 70).length, color: "#eab308" },
                { label: "Moderate (30-49)", count: Object.values(regions).filter((s: number) => s >= 30 && s < 50).length, color: "#22c55e" },
                { label: "Low (&lt;30)", count: Object.values(regions).filter((s: number) => s < 30).length, color: "#3b82f6" },
              ].map((item) => (
                <div key={item.label} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded" style={{ backgroundColor: item.color }} />
                    <span className="text-sm">{item.label}</span>
                  </div>
                  <span className="font-bold">{item.count} regions</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
