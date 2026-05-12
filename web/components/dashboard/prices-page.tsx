"use client"

import { useState, useEffect, useCallback } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { PriceChart } from "@/components/dashboard/price-chart"
import { RefreshButton } from "@/components/dashboard/refresh-button"
import { CountryConsumption } from "@/types"
import { Fuel } from "lucide-react"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export function PricesPage() {
  const [prices, setPrices] = useState<{ WTI: number; BRENT: number; DUBAI: number; OPEC_BASKET: number }>({ WTI: 0, BRENT: 0, DUBAI: 0, OPEC_BASKET: 0 })
  const [consumption, setConsumption] = useState<CountryConsumption[]>([])
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)
  const [loading, setLoading] = useState(true)

  const loadData = useCallback(async () => {
    try {
      const [pricesRes, consumptionRes] = await Promise.all([
        fetch(`${API_URL}/api/v1/prices/latest`).then(r => r.json()),
        fetch(`${API_URL}/api/v1/prices/consumption`).then(r => r.json()),
      ])
      
      const pricesArray = pricesRes.prices || []
      const pricesByType = { WTI: 0, BRENT: 0, DUBAI: 0, OPEC_BASKET: 0 }
      pricesArray.forEach((p: any) => {
        if (p.crude_type === "WTI") pricesByType.WTI = p.price
        if (p.crude_type === "BRENT") pricesByType.BRENT = p.price
        if (p.crude_type === "DUBAI") pricesByType.DUBAI = p.price
        if (p.crude_type === "OPEC_BASKET") pricesByType.OPEC_BASKET = p.price
      })
      
      setPrices(pricesByType)
      setConsumption(consumptionRes.data || [])
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
          <h1 className="text-3xl font-bold tracking-tight">Prices & Consumption</h1>
          <p className="text-muted-foreground">Global oil prices and consumption by country</p>
        </div>
        <RefreshButton onRefresh={loadData} lastUpdated={lastUpdated} />
      </div>

      <PriceChart prices={prices} />

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Top 20 Countries by Oil Consumption</CardTitle>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Fuel className="h-4 w-4" />
              <span>Million barrels/day & Price per liter</span>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-4 font-medium">Rank</th>
                  <th className="text-left py-3 px-4 font-medium">Country</th>
                  <th className="text-right py-3 px-4 font-medium">Consumption (MB/D)</th>
                  <th className="text-right py-3 px-4 font-medium">$/Barrel</th>
                  <th className="text-right py-3 px-4 font-medium">$/Liter (USD)</th>
                  <th className="text-right py-3 px-4 font-medium">Local Price</th>
                </tr>
              </thead>
              <tbody>
                {consumption.map((item) => (
                  <tr key={item.code} className="border-b hover:bg-muted/50">
                    <td className="py-3 px-4">
                      <span className={`font-bold ${
                        item.rank === 1 ? "text-yellow-500" :
                        item.rank === 2 ? "text-gray-400" :
                        item.rank === 3 ? "text-amber-600" : "text-muted-foreground"
                      }`}>
                        {item.rank}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-medium">{item.country}</td>
                    <td className="py-3 px-4 text-right">{item.consumption_mbd.toFixed(1)}</td>
                    <td className="py-3 px-4 text-right font-mono">${item.price_per_barrel_usd.toFixed(2)}</td>
                    <td className="py-3 px-4 text-right font-mono">${item.price_per_liter_usd.toFixed(4)}</td>
                    <td className="py-3 px-4 text-right">
                      <span className="font-mono">
                        {item.price_per_liter_local.toFixed(2)} {item.currency}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="p-4 rounded-lg bg-muted/50">
              <p className="text-sm text-muted-foreground">Total Consumption</p>
              <p className="text-2xl font-bold">
                {consumption.reduce((sum, c) => sum + c.consumption_mbd, 0).toFixed(1)} MB/D
              </p>
            </div>
            <div className="p-4 rounded-lg bg-muted/50">
              <p className="text-sm text-muted-foreground">Avg Price/Liter</p>
              <p className="text-2xl font-bold">
                ${(consumption.reduce((sum, c) => sum + c.price_per_liter_local, 0) / consumption.length).toFixed(2)}
              </p>
            </div>
            <div className="p-4 rounded-lg bg-muted/50">
              <p className="text-sm text-muted-foreground">Highest Consumer</p>
              <p className="text-2xl font-bold">{consumption[0]?.country}</p>
            </div>
            <div className="p-4 rounded-lg bg-muted/50">
              <p className="text-sm text-muted-foreground">Most Expensive</p>
              <p className="text-2xl font-bold">
                {consumption.reduce((max, c) => c.price_per_liter_local > max.price_per_liter_local ? c : max, consumption[0])?.country}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
