import { Link } from 'react-router-dom'
import type { AnalysisResult } from '../types/analysis'
import { Badge } from './Badge'
import { ProgressBar } from './ProgressBar'

interface RiskScoreProps {
  result: AnalysisResult
}

export function RiskScore({ result }: RiskScoreProps) {
  const isPhishing = result.prediction === 'phishing'
  const tone = isPhishing ? 'risk' : result.prediction === 'legitimate' ? 'safe' : 'warn'
  const label = result.prediction.toUpperCase()
  const confidencePct = (result.confidence * 100).toFixed(1)

  return (
    <section className="card overflow-hidden p-6 sm:p-8">
      <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
        <div className="max-w-2xl">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-muted">
            Analysis Result
          </p>
          <div className="mt-3 flex flex-wrap items-center gap-3">
            <h1 className={`text-4xl font-semibold sm:text-5xl ${isPhishing ? 'text-risk' : 'text-safe'}`}>
              {label}
            </h1>
            <Badge tone={tone}>{isPhishing ? 'High risk' : 'Low risk'}</Badge>
          </div>
          <p className="mt-4 font-mono text-2xl text-ink">{confidencePct}% confidence</p>
          <ProgressBar className="mt-4 max-w-md" value={result.confidence} tone={tone} />
          <p className="mt-5 break-all text-sm text-muted">
            URL:{' '}
            <span className="font-mono text-ink/90">{result.url}</span>
          </p>
          <p className="mt-3 text-sm leading-6 text-muted">{result.summary}</p>
        </div>
        <Link
          to="/"
          className="inline-flex h-11 shrink-0 items-center justify-center self-start rounded-xl border border-white/10 px-4 text-sm font-medium text-ink hover:bg-white/5"
        >
          New Analysis
        </Link>
      </div>
    </section>
  )
}
