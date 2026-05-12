"use client"

import { useState, useEffect, useCallback } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { NewsGrid } from "@/components/dashboard/news-card"
import { RefreshButton } from "@/components/dashboard/refresh-button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export default function NewsPage() {
  const [articles, setArticles] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)
  const [activeCategory, setActiveCategory] = useState("all")
  const [cached, setCached] = useState(false)

  const categories = [
    { value: "all", label: "All News" },
    { value: "positive", label: "Positive" },
    { value: "negative", label: "Negative" },
    { value: "neutral", label: "Neutral" },
  ]

  const loadNews = useCallback(async () => {
    try {
      const res = await fetch(`${API_URL}/api/v1/news?limit=30`)
      const data = await res.json()
      setArticles(data.articles || [])
      setCached(data.cached || false)
      setLastUpdated(new Date())
    } catch (error) {
      console.error("Failed to fetch news:", error)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadNews()
  }, [loadNews])

  const filteredArticles = articles.filter((article) => {
    if (activeCategory === "all") return true
    return article.sentiment?.toLowerCase() === activeCategory
  })

  const stats = {
    total: articles.length,
    positive: articles.filter((a) => a.sentiment?.toLowerCase() === "positive").length,
    negative: articles.filter((a) => a.sentiment?.toLowerCase() === "negative").length,
    neutral: articles.filter((a) => a.sentiment?.toLowerCase() === "neutral").length,
  }

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
          <h1 className="text-3xl font-bold tracking-tight">Energy News</h1>
          <p className="text-muted-foreground">
            Latest energy market news and sentiment analysis
          </p>
        </div>
        <RefreshButton onRefresh={loadNews} lastUpdated={lastUpdated} />
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Total Articles</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total}</div>
            {cached && <Badge variant="secondary" className="mt-1">Cached</Badge>}
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-green-600">Positive</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{stats.positive}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-red-600">Negative</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{stats.negative}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Neutral</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-600">{stats.neutral}</div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="all" onValueChange={setActiveCategory}>
        <TabsList>
          {categories.map((cat) => (
            <TabsTrigger key={cat.value} value={cat.value}>
              {cat.label}
            </TabsTrigger>
          ))}
        </TabsList>
        <TabsContent value={activeCategory} className="mt-4">
          <NewsGrid articles={filteredArticles} />
        </TabsContent>
      </Tabs>
    </div>
  )
}
