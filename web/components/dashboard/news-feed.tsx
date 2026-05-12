"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { NewsArticle } from "@/types"
import { ExternalLink, TrendingDown, TrendingUp, Minus } from "lucide-react"

interface NewsFeedProps {
  articles: NewsArticle[]
}

const SentimentIcon = ({ sentiment }: { sentiment: string }) => {
  if (sentiment === "bullish") return <TrendingUp className="h-4 w-4 text-green-500" />
  if (sentiment === "bearish") return <TrendingDown className="h-4 w-4 text-red-500" />
  return <Minus className="h-4 w-4 text-gray-400" />
}

const formatDate = (dateStr: string) => {
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  } catch {
    return dateStr
  }
}

export function NewsFeed({ articles }: NewsFeedProps) {
  return (
    <Card className="col-span-2">
      <CardHeader>
        <CardTitle>Energy News</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {articles.map((article, i) => (
            <div
              key={i}
              className="flex items-start gap-3 p-3 rounded-lg border hover:bg-accent/50 transition-colors"
            >
              <SentimentIcon sentiment={article.sentiment} />
              <div className="flex-1 min-w-0">
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="font-medium hover:underline line-clamp-2"
                >
                  {article.title}
                </a>
                {article.description && (
                  <p className="text-sm text-muted-foreground mt-1 line-clamp-2">
                    {article.description}
                  </p>
                )}
                <div className="flex items-center gap-2 mt-2 text-xs text-muted-foreground">
                  <span>{article.source}</span>
                  <span>•</span>
                  <span>{formatDate(article.published_at)}</span>
                </div>
              </div>
              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-foreground"
              >
                <ExternalLink className="h-4 w-4" />
              </a>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
