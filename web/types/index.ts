export interface PriceData {
  crude_type: "WTI" | "BRENT" | "DUBAI" | "OPEC_BASKET"
  price: number
  unit: string
  timestamp: string
}

export interface CountryConsumption {
  rank: number
  country: string
  code: string
  consumption_mbd: number
  consumption_twh: number
  price_per_barrel_usd: number
  price_per_liter_usd: number
  price_per_liter_local: number
  currency: string
}

export interface CountryRisk {
  code: string
  name: string
  risk: number
  lat: number
  lon: number
}

export interface PriceAnalytics {
  current: number
  ma_7: number
  ma_30: number
  volatility: number
  change_daily: number
  change_weekly: number
  high_30d: number
  low_30d: number
  anomalies: Anomaly[]
}

export interface Anomaly {
  timestamp: string
  price: number
  z_score: number
  type: "spike" | "drop"
}

export interface SentimentAnalysis {
  bullish_pct: number
  bearish_pct: number
  neutral_pct: number
  trend: "improving" | "declining"
  articles_analyzed: number
}

export interface RiskTrend {
  date: string
  score: number
  level: string
}

export interface EnergyForecast {
  region: string
  current: number
  forecast_1y: number
  growth_pct: number
}

export interface RiskScore {
  region: string | null
  global_score: number
  level: string
  factors: string[]
}

export interface ShipPosition {
  mmsi: string
  name: string
  latitude: number
  longitude: number
  heading: number | null
  speed: number | null
  timestamp: string
}

export interface EnergyConsumption {
  region: string
  country: string | null
  consumption_twh: number
  year: number
}

export interface Alert {
  id: string
  type: string
  message: string
  severity: string
  is_active: boolean
  created_at: string
}

export interface NewsArticle {
  title: string
  description: string | null
  source: string
  url: string
  published_at: string
  sentiment: string
}
