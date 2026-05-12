"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp, TrendingDown } from "lucide-react"

interface SentimentAnalysisProps {
  sentiment: {
    bullish_pct: number
    bearish_pct: number
    neutral_pct: number
    trend: string
    articles_analyzed: number
  }
}

export function SentimentAnalysisCard({ sentiment }: SentimentAnalysisProps) {
  const { bullish_pct, bearish_pct, neutral_pct, trend, articles_analyzed } = sentiment
  const isImproving = trend === "improving"

  return (
    <Card>
      <CardHeader>
        <CardTitle>Market Sentiment</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Overall Trend</span>
            <div className={`flex items-center gap-1 ${isImproving ? "text-green-500" : "text-red-500"}`}>
              {isImproving ? (
                <TrendingUp className="h-4 w-4" />
              ) : (
                <TrendingDown className="h-4 w-4" />
              )}
              <span className="text-sm font-medium capitalize">{trend}</span>
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-green-500" />
                Bullish
              </span>
              <span className="font-medium">{bullish_pct}%</span>
            </div>
            <div className="h-3 bg-muted rounded-full overflow-hidden">
              <div className="h-full bg-green-500 rounded-full" style={{ width: `${bullish_pct}%` }} />
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-red-500" />
                Bearish
              </span>
              <span className="font-medium">{bearish_pct}%</span>
            </div>
            <div className="h-3 bg-muted rounded-full overflow-hidden">
              <div className="h-full bg-red-500 rounded-full" style={{ width: `${bearish_pct}%` }} />
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-gray-400" />
                Neutral
              </span>
              <span className="font-medium">{neutral_pct}%</span>
            </div>
            <div className="h-3 bg-muted rounded-full overflow-hidden">
              <div className="h-full bg-gray-400 rounded-full" style={{ width: `${neutral_pct}%` }} />
            </div>
          </div>

          <p className="text-xs text-muted-foreground text-center pt-2">
            Based on {articles_analyzed} articles analyzed
          </p>
        </div>
      </CardContent>
    </Card>
  )
}
