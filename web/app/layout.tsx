import type { Metadata } from "next"
import { Geist, Geist_Mono } from "next/font/google"
import "./globals.css"
import { Fuel, BarChart3, Globe, Bell, Activity } from "lucide-react"
import Link from "next/link"

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
})

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
})

export const metadata: Metadata = {
  title: "GEIP - Global Energy Intelligence Platform",
  description: "Real-time energy market monitoring and analysis",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className="h-full">
      <body className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}>
        <div className="flex flex-col min-h-full">
          <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container flex h-16 items-center px-4">
              <div className="flex items-center gap-2 mr-8">
                <Fuel className="h-6 w-6 text-blue-600" />
                <span className="font-bold text-lg">GEIP</span>
              </div>
              <nav className="flex items-center gap-6 text-sm">
                <Link href="/" className="flex items-center gap-2 text-foreground hover:text-blue-600 transition-colors">
                  <BarChart3 className="h-4 w-4" />
                  Dashboard
                </Link>
                <Link href="/prices" className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
                  <Activity className="h-4 w-4" />
                  Prices
                </Link>
                <Link href="/risk" className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
                  <Globe className="h-4 w-4" />
                  Risk
                </Link>
                <Link href="/news" className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
                  <Bell className="h-4 w-4" />
                  News
                </Link>
              </nav>
            </div>
          </header>
          <main className="flex-1">
            {children}
          </main>
        </div>
      </body>
    </html>
  )
}
