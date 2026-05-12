"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface CountryRisk {
  code: string
  name: string
  risk: number
  lat: number
  lon: number
}

interface WorldHeatmapProps {
  countries: CountryRisk[]
}

function getRiskColor(risk: number): string {
  if (risk >= 75) return "#ef4444"
  if (risk >= 60) return "#f97316"
  if (risk >= 45) return "#eab308"
  if (risk >= 30) return "#22c55e"
  return "#3b82f6"
}

function getRiskLevel(risk: number): string {
  if (risk >= 75) return "Critical"
  if (risk >= 60) return "High"
  if (risk >= 45) return "Moderate"
  if (risk >= 30) return "Low"
  return "Minimal"
}

export function WorldHeatmap({ countries }: WorldHeatmapProps) {
  const [selectedCountry, setSelectedCountry] = useState<CountryRisk | null>(null)

  const worldMapWidth = 800
  const worldMapHeight = 400

  const latToY = (lat: number) => ((90 - lat) / 180) * worldMapHeight
  const lonToX = (lon: number) => ((lon + 180) / 360) * worldMapWidth

  return (
    <Card className="col-span-2">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Global Risk Heatmap</CardTitle>
          <div className="flex gap-2">
            <Badge style={{ backgroundColor: "#ef4444" }}>Critical</Badge>
            <Badge style={{ backgroundColor: "#f97316" }}>High</Badge>
            <Badge style={{ backgroundColor: "#eab308" }}>Moderate</Badge>
            <Badge style={{ backgroundColor: "#22c55e" }}>Low</Badge>
            <Badge style={{ backgroundColor: "#3b82f6" }}>Minimal</Badge>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="relative bg-slate-100 dark:bg-slate-800 rounded-lg overflow-hidden" style={{ width: "100%", height: "400px" }}>
          <svg viewBox={`0 0 ${worldMapWidth} ${worldMapHeight}`} className="w-full h-full">
            <rect x="0" y="0" width={worldMapWidth} height={worldMapHeight} fill="#e2e8f0" className="dark:fill-slate-700" />
            
            <g opacity="0.3" className="stroke-slate-400 dark:stroke-slate-600">
              <path d="M0,200 Q200,100 400,200 T800,200" fill="none" strokeWidth="1" />
              <path d="M0,100 Q200,200 400,100 T800,100" fill="none" strokeWidth="1" />
              <path d="M0,300 Q200,200 400,300 T800,300" fill="none" strokeWidth="1" />
              <line x1="0" y1="200" x2="800" y2="200" strokeWidth="0.5" strokeDasharray="4" />
              <line x1="400" y1="0" x2="400" y2="400" strokeWidth="0.5" strokeDasharray="4" />
            </g>
            
            {countries.map((country) => {
              const x = lonToX(country.lon)
              const y = latToY(country.lat)
              const size = 12 + (country.risk / 100) * 20

              return (
                <g
                  key={country.code}
                  onClick={() => setSelectedCountry(country)}
                  className="cursor-pointer"
                >
                  <circle
                    cx={x}
                    cy={y}
                    r={size / 2}
                    fill={getRiskColor(country.risk)}
                    fillOpacity="0.7"
                    stroke={getRiskColor(country.risk)}
                    strokeWidth="2"
                    className="hover:fill-opacity-100 transition-all"
                  />
                </g>
              )
            })}
          </svg>

          {selectedCountry && (
            <div className="absolute top-4 left-4 bg-white dark:bg-slate-900 p-4 rounded-lg shadow-lg border">
              <h3 className="font-bold">{selectedCountry.name}</h3>
              <div className="mt-2 space-y-1">
                <p className="text-sm">
                  Risk Score: <span className="font-medium" style={{ color: getRiskColor(selectedCountry.risk) }}>{selectedCountry.risk}</span>
                </p>
                <p className="text-sm">
                  Level: <Badge style={{ backgroundColor: getRiskColor(selectedCountry.risk) }}>{getRiskLevel(selectedCountry.risk)}</Badge>
                </p>
              </div>
              <button
                onClick={() => setSelectedCountry(null)}
                className="mt-2 text-xs text-muted-foreground hover:text-foreground"
              >
                Close
              </button>
            </div>
          )}
        </div>

        <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-2">
          {countries.slice(0, 8).map((country) => (
            <div
              key={country.code}
              className="p-2 rounded bg-muted/50 flex items-center justify-between"
            >
              <span className="text-sm">{country.name}</span>
              <span
                className="font-medium text-sm"
                style={{ color: getRiskColor(country.risk) }}
              >
                {country.risk}
              </span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
