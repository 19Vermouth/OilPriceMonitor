const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

async function fetchAPI<T>(endpoint: string): Promise<T> {
  const res = await fetch(`${API_URL}${endpoint}`, {
    next: { revalidate: 300 },
  })
  
  if (!res.ok) {
    throw new Error(`API error: ${res.status}`)
  }
  
  return res.json()
}

export async function getPrices() {
  const data = await fetchAPI<{ prices: any[] }>("/api/v1/prices/latest")
  return data.prices
}

export async function getPriceHistory(crudeType: string = "WTI", days: number = 30) {
  const data = await fetchAPI<{ prices: any[] }>(
    `/api/v1/prices/history?crude_type=${crudeType}&days=${days}`
  )
  return data.prices
}

export async function getCountryConsumption() {
  const data = await fetchAPI<{ data: any[] }>("/api/v1/prices/consumption")
  return data.data
}

export async function getGlobalRisk() {
  return fetchAPI<any>("/api/v1/risk/global")
}

export async function getRegionalRisk(region: string) {
  return fetchAPI<any>(`/api/v1/risk/region/${region}`)
}

export async function getRiskHeatmap() {
  return fetchAPI<any>("/api/v1/risk/heatmap")
}

export async function getShips() {
  const data = await fetchAPI<{ ships: any[] }>("/api/v1/ships/live")
  return data.ships
}

export async function getEnergyConsumption() {
  const data = await fetchAPI<{ data: any[] }>("/api/v1/energy/consumption")
  return data.data
}

export async function getAlerts() {
  const data = await fetchAPI<{ alerts: any[] }>("/api/v1/alerts/active")
  return data.alerts
}

export async function getNews(limit: number = 10) {
  const data = await fetchAPI<{ articles: any[] }>(`/api/v1/news/news?limit=${limit}`)
  return data.articles
}

export async function getPriceAnalytics() {
  return fetchAPI<any>("/api/v1/analytics/prices")
}

export async function getSentimentAnalysis() {
  return fetchAPI<any>("/api/v1/analytics/sentiment")
}

export async function getRiskTrend() {
  const data = await fetchAPI<{ trends: any[] }>("/api/v1/analytics/risk/trend")
  return data.trends
}

export async function getEnergyForecast() {
  const data = await fetchAPI<{ forecast: any[] }>("/api/v1/analytics/energy/forecast")
  return data.forecast
}

export async function getAnalyticsSummary() {
  return fetchAPI<any>("/api/v1/analytics/summary")
}
