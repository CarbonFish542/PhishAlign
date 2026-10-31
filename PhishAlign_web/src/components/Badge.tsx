import type { ReactNode } from 'react'

export type BadgeTone = 'risk' | 'safe' | 'warn' | 'info' | 'neutral'

const toneClass: Record<BadgeTone, string> = {
  risk: 'bg-risk/15 text-risk border-risk/25',
  safe: 'bg-safe/15 text-safe border-safe/25',
  warn: 'bg-warn/15 text-warn border-warn/25',
  info: 'bg-cyan/15 text-cyan border-cyan/25',
  neutral: 'bg-white/5 text-muted border-white/10',
}

interface BadgeProps {
  children: ReactNode
  tone?: BadgeTone
  className?: string
}

export function Badge({ children, tone = 'neutral', className = '' }: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-[11px] font-semibold uppercase tracking-wide ${toneClass[tone]} ${className}`}
    >
      {children}
    </span>
  )
}
