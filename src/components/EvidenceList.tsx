import { AlertCircle, AlertTriangle, Info } from 'lucide-react'
import type { EvidenceItem, ImpactLevel } from '../types/analysis'
import { Badge, type BadgeTone } from './Badge'

interface EvidenceListProps {
  items: EvidenceItem[]
  title?: string
}

const impactMeta: Record<ImpactLevel, { label: string; tone: BadgeTone; icon: typeof AlertTriangle }> = {
  high: { label: 'High impact', tone: 'risk', icon: AlertTriangle },
  medium: { label: 'Medium impact', tone: 'warn', icon: AlertCircle },
  low: { label: 'Low impact', tone: 'info', icon: Info },
}

const order: ImpactLevel[] = ['high', 'medium', 'low']

export function EvidenceList({ items, title = 'Why was this classified as phishing?' }: EvidenceListProps) {
  return (
    <section className="card p-5 sm:p-6">
      <h3 className="text-lg font-semibold">{title}</h3>
      <div className="mt-5 space-y-6">
        {order.map((level) => {
          const group = items.filter((item) => item.impact === level)
          if (group.length === 0) return null
          const meta = impactMeta[level]
          const Icon = meta.icon
          return (
            <div key={level}>
              <div className="mb-3 flex items-center gap-2">
                <Icon className="h-4 w-4 text-muted" aria-hidden />
                <p className="text-xs font-semibold uppercase tracking-wide text-muted">{meta.label}</p>
              </div>
              <ul className="space-y-2">
                {group.map((item) => (
                  <li
                    key={item.id}
                    className="flex flex-col gap-2 rounded-xl border border-white/6 bg-navy-950/40 p-3 sm:flex-row sm:items-center sm:justify-between"
                  >
                    <div>
                      <p className="text-sm text-ink">{item.description}</p>
                      <p className="mt-1 text-xs text-muted">{item.category}</p>
                    </div>
                    <div className="flex gap-2">
                      <Badge tone={meta.tone}>{item.impact}</Badge>
                      <Badge>{item.modality}</Badge>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )
        })}
      </div>
    </section>
  )
}
