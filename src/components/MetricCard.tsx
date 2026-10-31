import type { LucideIcon } from 'lucide-react'
import type { ReactNode } from 'react'

interface MetricCardProps {
  icon?: LucideIcon
  label: string
  value: ReactNode
  hint?: string
}

export function MetricCard({ icon: Icon, label, value, hint }: MetricCardProps) {
  return (
    <div className="rounded-xl border border-white/6 bg-navy-950/40 p-4">
      <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-muted">
        {Icon ? <Icon className="h-3.5 w-3.5 text-cyan" aria-hidden /> : null}
        {label}
      </div>
      <div className="mt-2 font-mono text-lg text-ink">{value}</div>
      {hint ? <p className="mt-1 text-xs text-muted">{hint}</p> : null}
    </div>
  )
}
