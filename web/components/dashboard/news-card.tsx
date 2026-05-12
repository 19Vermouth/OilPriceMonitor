"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

interface Article {
  title: string
  description: string | null
  url: string
  source: { name: string }
  publishedAt: string
  sentiment?: string
  sentiment_score?: number
}

interface NewsCardProps {
  article: Article
  index: number
}

function getSentimentColor(sentiment?: string) {
  switch (sentiment?.toLowerCase()) {
    case "positive":
      return "text-green-600"
    case "negative":
      return "text-red-600"
    default:
      return "text-gray-600"
  }
}

function getSentimentBg(sentiment?: string) {
  switch (sentiment?.toLowerCase()) {
    case "positive":
      return "bg-green-100 dark:bg-green-900"
    case "negative":
      return "bg-red-100 dark:bg-red-900"
    default:
      return "bg-gray-100 dark:bg-gray-800"
  }
}

function formatDate(dateStr: string) {
  const date = new Date(dateStr)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))

  if (diffHours < 1) return "Just now"
  if (diffHours < 24) return `${diffHours}h ago`
  const diffDays = Math.floor(diffHours / 24)
  if (diffDays < 7) return `${diffDays}d ago`
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric" })
}

export function NewsCard({ article, index }: NewsCardProps) {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-2">
        <div className="flex justify-between items-start gap-2">
          <div className="space-y-1">
            <CardTitle className="text-base line-clamp-2">
              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:underline"
              >
                {article.title}
              </a>
            </CardTitle>
            <CardDescription className="flex items-center gap-2 text-xs">
              <span className="font-medium">{article.source.name}</span>
              <span>•</span>
              <span>{formatDate(article.publishedAt)}</span>
            </CardDescription>
          </div>
          {article.sentiment && (
            <span
              className={`px-2 py-1 rounded text-xs font-medium ${getSentimentBg(
                article.sentiment
              )} ${getSentimentColor(article.sentiment)}`}
            >
              {article.sentiment}
            </span>
          )}
        </div>
      </CardHeader>
      {article.description && (
        <CardContent>
          <p className="text-sm text-muted-foreground line-clamp-3">
            {article.description}
          </p>
          {article.sentiment_score !== undefined && (
            <div className="mt-2 flex items-center gap-2">
              <span className="text-xs text-muted-foreground">Score:</span>
              <div className="flex-1 h-1.5 bg-muted rounded-full overflow-hidden max-w-20">
                <div
                  className="h-full rounded-full"
                  style={{
                    width: `${Math.abs(article.sentiment_score) * 100}%`,
                    backgroundColor:
                      article.sentiment_score > 0 ? "#22c55e" : article.sentiment_score < 0 ? "#ef4444" : "#6b7280",
                  }}
                />
              </div>
              <span className="text-xs font-medium">
                {(article.sentiment_score * 100).toFixed(0)}%
              </span>
            </div>
          )}
        </CardContent>
      )}
    </Card>
  )
}

interface NewsGridProps {
  articles: Article[]
}

export function NewsGrid({ articles }: NewsGridProps) {
  if (!articles || articles.length === 0) {
    return (
      <Card>
        <CardContent className="py-8 text-center text-muted-foreground">
          No news articles available
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {articles.map((article, index) => (
        <NewsCard key={`${article.url}-${index}`} article={article} index={index} />
      ))}
    </div>
  )
}
