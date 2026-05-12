"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { RiskScore } from "@/types"
import { AlertTriangle } from "lucide-react"

interface RiskDisplayProps {
  risk: RiskScore
}

const getRiskColor = (score: number) => {
  if (score >= 70) return "text-red-500"
  if (score >= 50) return "text-yellow-500"
  return "text-green-500"
}

const getRiskBg = (score: number) => {
  if (score >= 70) return "bg-red-500/10"
  if (score >= 50) return "bg-yellow-500/10"
  return "bg-green-500/10"
}

export function RiskDisplay({ risk }: RiskDisplayProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-base font-medium">Global Risk Score</CardTitle>
        <AlertTriangle className={`h-5 w-5 ${getRiskColor(risk.global_score)}`} />
      </CardHeader>
      <CardContent>
        <div className={`text-4xl font-bold ${getRiskColor(risk.global_score)}`}>
          {risk.global_score.toFixed(1)}
        </div>
        <p className="text-xs text-muted-foreground mt-1">{risk.level} Risk</p>
        <div className={`mt-4 p-3 rounded-lg ${getRiskBg(risk.global_score)}`}>
          <p className="text-sm font-medium mb-2">Contributing Factors:</p>
          <ul className="text-xs space-y-1">
            {risk.factors.map((factor, i) => (
              <li key={i} className="flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-current opacity-50" />
                {factor}
              </li>
            ))}
          </ul>
        </div>
      </CardContent>
    </Card>
  )
}
