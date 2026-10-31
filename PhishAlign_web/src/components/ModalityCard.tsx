import type { LucideIcon } from 'lucide-react'
import { ProgressBar } from './ProgressBar'

interface ModalityCardProps {
  icon: LucideIcon
  title: string
  probability: number
  explanation: string
  available?: boolean
}

function probabilityTone(probability: number): 'risk' | 'warn' | 'safe' {
  if (probability >= 0.6) return 'risk'
  if (probability >= 0.3) return 'warn'
  return 'safe'
}

export function ModalityCard({
  icon: Icon,
  title,
  probability,
  explanation,
  available = true,
}: ModalityCardProps) {
  if (!available) {
    return (
      <article className="card p-5">
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-muted">
          <Icon className="h-4 w-4 text-cyan" aria-hidden />
          {title}
        </div>
        <p className="mt-4 text-sm text-warn">This modality is unavailable.</p>
      </article>
    )
  }

  const pct = (probability * 100).toFixed(1)
  const tone = probabilityTone(probability)

  return (
    <article className="card animate-fade-up p-5">
      <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-muted">
        <Icon className="h-4 w-4 text-cyan" aria-hidden />
        {title}
      </div>
      <p className="mt-3 font-mono text-3xl text-ink">{pct}%</p>
      <p className="mt-1 text-xs text-muted">phishing probability</p>
      <ProgressBar className="mt-4" value={probability} tone={tone} />
      <p className="mt-4 text-sm leading-6 text-muted">{explanation}</p>
    </article>
  )
}
