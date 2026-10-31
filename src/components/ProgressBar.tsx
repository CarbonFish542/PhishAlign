interface ProgressBarProps {
  value: number
  max?: number
  tone?: 'risk' | 'safe' | 'warn' | 'info' | 'neutral'
  className?: string
  label?: string
}

const fillClass = {
  risk: 'bg-risk',
  safe: 'bg-safe',
  warn: 'bg-warn',
  info: 'bg-cyan',
  neutral: 'bg-muted',
}

export function ProgressBar({
  value,
  max = 1,
  tone = 'info',
  className = '',
  label,
}: ProgressBarProps) {
  const pct = Math.max(0, Math.min(100, (value / max) * 100))

  return (
    <div className={className}>
      {label ? (
        <div className="mb-1.5 flex items-center justify-between text-xs text-muted">
          <span>{label}</span>
          <span className="font-mono text-ink/80">{pct.toFixed(1)}%</span>
        </div>
      ) : null}
      <div
        className="h-2 overflow-hidden rounded-full bg-navy-950/80 ring-1 ring-white/5"
        role="progressbar"
        aria-valuenow={Number(pct.toFixed(1))}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <div
          className={`h-full rounded-full transition-[width] duration-700 ease-out ${fillClass[tone]}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}
