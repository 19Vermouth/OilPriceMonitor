"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { RefreshCw, Loader2 } from "lucide-react"

interface RefreshButtonProps {
  onRefresh: () => void
  lastUpdated: Date | null
}

export function RefreshButton({ onRefresh, lastUpdated }: RefreshButtonProps) {
  const [loading, setLoading] = useState(false)

  const handleRefresh = async () => {
    setLoading(true)
    await onRefresh()
    setLoading(false)
  }

  return (
    <div className="flex items-center gap-2">
      {lastUpdated && (
        <span className="text-sm text-muted-foreground">
          Last updated: {lastUpdated.toLocaleTimeString()}
        </span>
      )}
      <Button variant="outline" size="sm" onClick={handleRefresh} disabled={loading}>
        {loading ? (
          <Loader2 className="h-4 w-4 animate-spin" />
        ) : (
          <RefreshCw className="h-4 w-4" />
        )}
        <span className="ml-2">Refresh</span>
      </Button>
    </div>
  )
}
