
import type { IdentityAnalysisData, ConsistencyScores } from '../types/analysis'

interface IdentityAnalysisProps {
  identities: IdentityAnalysisData
  consistency: ConsistencyScores
}

function formatOverlap(value: number | null | undefined): string {
  if (value == null || !Number.isFinite(value)) return 'Unavailable'
  return `${(value * 100).toFixed(1)}%`
}

export function IdentityAnalysis({
  identities,
  consistency,
}: IdentityAnalysisProps) {
  const comparisons = [
    {
      label: 'Domain ↔ HTML',
      value: consistency.domain_html,
      available: consistency.domain_html_available,
    },
    {
      label: 'Domain ↔ Screenshot OCR',
      value: consistency.domain_ocr,
      available: consistency.domain_ocr_available,
    },
    {
      label: 'Domain ↔ Page title',
      value: consistency.domain_title,
      available: consistency.domain_title_available,
    },
  ]

  return (
    <section className="card p-5 sm:p-6">
      <h3 className="text-lg font-semibold">Website Identity Signals</h3>

      <p className="mt-2 text-sm leading-6 text-muted">
        These signals compare tokens from the website domain with page content.
        They measure text overlap, not verified brand identity. Low overlap
        alone does not establish that a website is phishing.
      </p>

      <dl className="mt-5 grid gap-4 sm:grid-cols-3">
        <div className="rounded-xl bg-navy-950/50 p-4">
          <dt className="text-xs font-medium uppercase tracking-wide text-muted">
            URL domain
          </dt>
          <dd className="mt-2 break-all font-mono text-sm">
            {identities.url || 'Unavailable'}
          </dd>
        </div>

        <div className="rounded-xl bg-navy-950/50 p-4">
          <dt className="text-xs font-medium uppercase tracking-wide text-muted">
            HTML page title
          </dt>
          <dd className="mt-2 break-words text-sm">
            {identities.html || 'Unavailable'}
          </dd>
        </div>

        <div className="rounded-xl bg-navy-950/50 p-4">
          <dt className="text-xs font-medium uppercase tracking-wide text-muted">
            Screenshot OCR
          </dt>
          <dd className="mt-2 text-sm">
            {identities.visual || 'Unavailable'}
          </dd>
        </div>
      </dl>

      <div className="mt-6">
        <h4 className="text-sm font-semibold">Domain Identity Overlap</h4>

        <div className="mt-3 space-y-3">
          {comparisons.map((item) => {
            const usable = item.available !== false && item.value != null

            return (
              <div
                key={item.label}
                className="flex flex-wrap items-center justify-between gap-3 rounded-xl bg-navy-950/50 p-4"
              >
                <span className="text-sm">{item.label}</span>
                <span className="font-mono text-sm">
                  {usable ? formatOverlap(item.value) : 'Unavailable'}
                </span>
              </div>
            )
          })}
        </div>
      </div>

      <p className="mt-4 text-xs leading-5 text-muted">
        Jaccard overlap is calculated from token sets. A high score does not
        guarantee legitimacy, and a low score does not prove phishing.
        PhishAlign's final prediction combines modality probabilities with
        cross-modal consistency features.
      </p>
    </section>
  )
}
