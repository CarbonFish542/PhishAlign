import { Link } from 'react-router-dom'
import type { AnalysisResult } from '../types/analysis'
import { Badge } from './Badge'
import { ProgressBar } from './ProgressBar'

interface RiskScoreProps {
  result: AnalysisResult
}

export function RiskScore({ result }: RiskScoreProps) {
  const probability = result.confidence
  const confidencePct = (probability * 100).toFixed(1)

  const riskLevel =
    probability >= 0.8
      ? {
          label: 'High phishing risk',
          heading: 'HIGH PHISHING RISK',
          tone: 'risk' as const,
          description:
            'PhishAlign assigns this page a high phishing score. Avoid entering passwords or sensitive information unless you can independently verify the website.',
        }
      : probability >= 0.5
        ? {
            label: 'Suspicious',
            heading: 'SUSPICIOUS',
            tone: 'warn' as const,
            description:
              'PhishAlign detected a potential phishing risk. Review the evidence carefully before trusting this website.',
          }
        : {
            label: 'Likely legitimate',
            heading: 'LIKELY LEGITIMATE',
            tone: 'safe' as const,
            description:
              'PhishAlign assigns this page a lower phishing score. This does not guarantee that the website is safe.',
          }

  return (
    <section className="card overflow-hidden p-6 sm:p-8">
      <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
        <div className="max-w-2xl">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-muted">
            Analysis Result
          </p>

          <div className="mt-3 flex flex-wrap items-center gap-3">
            <h1
              className={`text-3xl font-semibold sm:text-4xl ${
                riskLevel.tone === 'risk'
                  ? 'text-risk'
                  : riskLevel.tone === 'warn'
                    ? 'text-amber-400'
                    : 'text-safe'
              }`}
            >
              {riskLevel.heading}
            </h1>
            <Badge tone={riskLevel.tone}>{riskLevel.label}</Badge>
          </div>

          <p className="mt-4 font-mono text-2xl text-ink">
            {confidencePct}% phishing probability
          </p>

          <ProgressBar
            className="mt-4 max-w-md"
            value={probability}
            tone={riskLevel.tone}
          />

          <p className="mt-5 break-all text-sm text-muted">
            URL:{' '}
            <span className="font-mono text-ink/90">{result.url}</span>
          </p>

          <p className="mt-3 text-sm leading-6 text-muted">
            {riskLevel.description}
          </p>

          <p className="mt-2 text-xs leading-5 text-muted">
            Risk levels: below 50% = likely legitimate; 50% to below 80% =
            suspicious; 80% and above = high phishing risk. These are model
            thresholds, not guarantees of website safety or maliciousness.
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