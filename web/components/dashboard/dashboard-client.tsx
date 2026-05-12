"use client"

import { useState, useCallback, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { PriceChart } from "@/components/dashboard/price-chart"
import { RiskDisplay } from "@/components/dashboard/risk-display"
import { NewsFeed } from "@/components/dashboard/news-feed"
import { AlertsList } from "@/components/dashboard/alerts-list"
import { EnergyChart } from "@/components/dashboard/energy-chart"
import { DashboardStats } from "@/components/dashboard/dashboard-stats"
import { RefreshButton } from "@/components/dashboard/refresh-button"
import { PriceAnalyticsCard } from "@/components/dashboard/price-analytics"
import { SentimentAnalysisCard } from "@/components/dashboard/sentiment-analysis"
import { RiskTrendChart } from "@/components/dashboard/risk-trend"
import { AnomalyCard } from "@/components/dashboard/anomaly-detection"
import { EnergyForecastCard } from "@/components/dashboard/energy-forecast"
import { PriceData, RiskScore, NewsArticle, Alert, EnergyConsumption } from "@/types"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

async function fetchData() {
  const [pricesRes, riskRes, newsRes, alertsRes, energyRes, analyticsRes] = await Promise.all([
    fetch(`${API_URL}/api/v1/prices/latest`).then(r => r.json()),
    fetch(`${API_URL}/api/v1/risk/global`).then(r => r.json()),
    fetch(`${API_URL}/api/v1/news/news?limit=10`).then(r => r.json()),
    fetch(`${API_URL}/api/v1/alerts/active`).then(r => r.json()),
    fetch(`${API_URL}/api/v1/energy/consumption`).then(r => r.json()),
    fetch(`${API_URL}/api/v1/analytics/summary`).then(r => r.json()),
  ])

  const pricesArray = pricesRes.prices || []
  const pricesByType = {
    WTI: 0,
    BRENT: 0,
    DUBAI: 0,
    OPEC_BASKET: 0,
  }
  
  pricesArray.forEach((p: any) => {
    if (p.crude_type === "WTI") pricesByType.WTI = p.price
    if (p.crude_type === "BRENT") pricesByType.BRENT = p.price
    if (p.crude_type === "DUBAI") pricesByType.DUBAI = p.price
    if (p.crude_type === "OPEC_BASKET") pricesByType.OPEC_BASKET = p.price
  })

  return {
    prices: pricesByType,
    risk: riskRes,
    news: newsRes.articles || [],
    alerts: alertsRes.alerts || [],
    energy: energyRes.data || [],
    analytics: analyticsRes || {},
  }
}

export function Dashboard() {
  const [prices, setPrices] = useState<{ WTI: number; BRENT: number; DUBAI: number; OPEC_BASKET: number }>({ WTI: 0, BRENT: 0, DUBAI: 0, OPEC_BASKET: 0 })
  const [risk, setRisk] = useState<RiskScore | null>(null)
  const [news, setNews] = useState<NewsArticle[]>([])
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [energy, setEnergy] = useState<EnergyConsumption[]>([])
  const [analytics, setAnalytics] = useState<any>({})
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)
  const [loading, setLoading] = useState(true)

  const loadData = useCallback(async () => {
    try {
      const data = await fetchData()
      setPrices(data.prices)
      setRisk(data.risk)
      setNews(data.news)
      setAlerts(data.alerts)
      setEnergy(data.energy)
      setAnalytics(data.analytics)
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
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground">Real-time energy market overview</p>
        </div>
        <RefreshButton onRefresh={loadData} lastUpdated={lastUpdated} />
      </div>

      <DashboardStats prices={prices} risk={risk} alerts={alerts} />

      <div className="grid gap-4 md:grid-cols-3">
        <PriceChart prices={prices} />
        <RiskDisplay risk={risk || { global_score: 0, level: "Unknown", factors: [], region: null }} />
        <AnomalyCard analytics={analytics.prices || {}} />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <PriceAnalyticsCard analytics={analytics.prices || {}} />
        <SentimentAnalysisCard sentiment={analytics.sentiment || { bullish_pct: 0, bearish_pct: 0, neutral_pct: 100, trend: "neutral", articles_analyzed: 0 }} />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <NewsFeed articles={news} />
        <AlertsList alerts={alerts} />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <RiskTrendChart trends={analytics.risk_trend || []} />
        <EnergyForecastCard forecast={analytics.energy_forecast || []} />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <EnergyChart data={energy} />
        <Card>
          <CardHeader>
            <CardTitle>Risk by Region</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {[
                { region: "Middle East", risk: 78 },
                { region: "Africa", risk: 68 },
                { region: "Asia Pacific", risk: 55 },
                { region: "Latin America", risk: 52 },
                { region: "Europe", risk: 42 },
                { region: "North America", risk: 35 },
              ].map((item) => (
                <div key={item.region} className="flex items-center justify-between">
                  <span className="text-sm">{item.region}</span>
                  <div className="flex items-center gap-2">
                    <div className="w-24 h-2 bg-muted rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full"
                        style={{
                          width: `${item.risk}%`,
                          backgroundColor: item.risk >= 70 ? "#ef4444" : item.risk >= 50 ? "#eab308" : "#22c55e",
                        }}
                      />
                    </div>
                    <span className="text-sm font-medium w-8">{item.risk}</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
