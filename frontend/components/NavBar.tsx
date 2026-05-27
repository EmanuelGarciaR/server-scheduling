"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"

const LINKS = [
  { href: "/",           label: "Dashboard"   },
  { href: "/benchmarks", label: "Benchmarks"  },
]

export default function NavBar() {
  const pathname = usePathname()

  return (
    <nav className="border-b border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900">
      <div className="max-w-6xl mx-auto px-6 md:px-10 flex items-center gap-6 h-12">
        <span className="text-sm font-semibold text-neutral-800 dark:text-neutral-200 mr-2">
          Server Scheduling
        </span>
        {LINKS.map(({ href, label }) => {
          const active = pathname === href
          return (
            <Link
              key={href}
              href={href}
              className={`text-sm transition-colors ${
                active
                  ? "text-neutral-900 dark:text-neutral-100 font-medium border-b-2 border-blue-600 pb-px"
                  : "text-neutral-500 dark:text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-300"
              }`}
            >
              {label}
            </Link>
          )
        })}
      </div>
    </nav>
  )
}
