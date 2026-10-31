import { useState } from 'react'
import { Code2, Eye, GitCompare, LayoutList, Link2, Sparkles } from 'lucide-react'
import type { AnalysisResult } from '../types/analysis'
import { ConsistencyGraph } from './ConsistencyGraph'
import { ConsistencyMatrix } from './ConsistencyMatrix'
import { EvidenceList } from './EvidenceList'
import { IdentityAnalysis } from './IdentityAnalysis'
import { MetricCard } from './MetricCard'
import { SHAPChart } from './SHAPChart'
import { WebsitePreview } from './WebsitePreview'
import { Badge } from './Badge'

const tabs = [
  { id: 'overview', label: 'Overview', icon: LayoutList },
  { id: 'url', label: 'URL', icon: Link2 },
  { id: 'html', label: 'HTML', icon: Code2 },
  { id: 'visual', label: 'Visual', icon: Eye },
  { id: 'consistency', label: 'Consistency', icon: GitCompare },
  { id: 'explainability', label: 'Explainability', icon: Sparkles },
] as const

type TabId = (typeof tabs)[number]['id']

interface AnalysisTabsProps {
  result: AnalysisResult
}

export function AnalysisTabs({ result }: AnalysisTabsProps) {
  const [active, setActive] = useState<TabId>('overview')

  const visualFeatures = result.modalities.visual.features

  const ocrStatus =
    visualFeatures.visualEvidence
      .find((item) => item.startsWith('OCR status:'))
      ?.replace('OCR status: ', '') ?? 'unknown'

  const ocrCharacterCount = Number(
    visualFeatures.visualEvidence
      .find((item) => item.startsWith('OCR characters extracted:'))
      ?.replace('OCR characters extracted: ', '') ?? 0,
  )

  const highImpactEvidence = result.evidence

  return (
    <div>
      <div
        role="tablist"
        aria-label="Detailed analysis"
        className="flex gap-1 overflow-x-auto rounded-xl border border-white/6 bg-navy-850 p-1"
      >
        {tabs.map((tab) => {
          const Icon = tab.icon
          const selected = active === tab.id

          return (
            <button
              key={tab.id}
              type="button"
              role="tab"
              aria-selected={selected}
              onClick={() => setActive(tab.id)}
              className={`inline-flex shrink-0 items-center gap-2 rounded-lg px-3 py-2 text-sm ${
                selected ? 'bg-navy-700 text-ink' : 'text-muted hover:text-ink'
              }`}
            >
              <Icon className="h-4 w-4" aria-hidden />
              {tab.label}
            </button>
          )
        })}
      </div>

      <div className="mt-5 space-y-5" role="tabpanel">
        {active === 'overview' ? (
          <>
            <WebsitePreview
              url={result.url}
              visual={visualFeatures}
              visualProbability={result.modalities.visual.probability}
              available={result.modalities.visual.available}
              ocrStatus={ocrStatus}
              ocrCharacterCount={ocrCharacterCount}
            />

            <ConsistencyGraph
              scores={result.consistency}
              interpretation={result.summary}
            />

            <IdentityAnalysis
              identities={result.identities}
              consistency={result.consistency}
            />

            {highImpactEvidence.length > 0 ? (
              <EvidenceList
                items={highImpactEvidence}
                title={
                  'Live analysis evidence'
                }
              />
            ) : (
              <section className="card p-5 sm:p-6">
                  <h3 className="text-lg font-semibold">
                    No additional evidence returned
                  </h3>
                <p className="mt-2 text-sm leading-6 text-muted">
                  The live API does not currently return rule-level evidence
                  or per-feature explanations for this prediction. Review the
                  model probabilities and consistency analysis for the
                  available results.
                </p>
              </section>
            )}
          </>
        ) : null}

        {active === 'url' ? (
          <section className="card p-5 sm:p-6">
            <div className="flex items-center justify-between gap-3">
              <h3 className="text-lg font-semibold">URL Analysis</h3>
              <Badge tone="info">
                {(result.modalities.url.probability * 100).toFixed(1)}%
                {' '}phishing probability
              </Badge>
            </div>

            <p className="mt-2 break-all font-mono text-sm text-muted">
              {result.modalities.url.features.fullUrl}
            </p>

            <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              <MetricCard
                label="Domain"
                value={result.modalities.url.features.domain}
              />
              <MetricCard
                label="HTTPS"
                value={result.modalities.url.features.https ? 'Yes' : 'No'}
              />
              <MetricCard
                label="URL length"
                value={result.modalities.url.features.length}
              />
              <MetricCard
                label="Subdomains"
                value={result.modalities.url.features.subdomainCount}
              />
              <MetricCard
                label="Entropy"
                value={result.modalities.url.features.entropy.toFixed(2)}
              />
              <MetricCard
                label="Special characters"
                value={result.modalities.url.features.specialCharacterCount}
              />
            </div>

            <div className="mt-5">
              <p className="mt-2 text-xs text-muted">
                Token presence alone does not establish phishing and is not an individual SHAP attribution.
              </p>
              <div className="mt-2 flex flex-wrap gap-2">
                {result.modalities.url.features.suspiciousTokens.length === 0 ? (
                  <span className="text-sm text-muted">
                    No configured tokens found in this URL.
                  </span>
                ) : (
                  result.modalities.url.features.suspiciousTokens.map(
                    (token) => (
                      <span
                        key={token}
                        className="rounded-md bg-risk/10 px-2 py-1 font-mono text-xs text-risk"
                      >
                        {token}
                      </span>
                    ),
                  )
                )}
              </div>
            </div>
          </section>
        ) : null}

        {active === 'html' ? (
          <section className="card p-5 sm:p-6">
            <div className="flex items-center justify-between gap-3">
              <h3 className="text-lg font-semibold">HTML Analysis</h3>
              <Badge tone="info">
                {(result.modalities.html.probability * 100).toFixed(1)}%
                {' '}phishing probability
              </Badge>
            </div>

            <div className="mt-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-muted">
                Page title
              </p>
              <p className="mt-2 break-words text-sm">
                {result.modalities.html.features.pageTitle ||
                  'Page title unavailable'}
              </p>
            </div>

            
<div className="mt-5 rounded-xl border border-white/10 bg-navy-850 p-4">
  <h4 className="font-medium">HTML structural metrics</h4>
  <p className="mt-1 text-sm text-muted">
    Counts extracted from the captured HTML. These indicators are descriptive
    and do not independently establish that a website is malicious.
  </p>

  <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3">
    {[
      { label: 'Forms', value: result.modalities.html.features.formCount },
      {
        label: 'Password fields',
        value: result.modalities.html.features.passwordFields,
      },
      {
        label: 'External links',
        value: result.modalities.html.features.externalLinks,
      },
      { label: 'Iframes', value: result.modalities.html.features.iframes },
      { label: 'Scripts', value: result.modalities.html.features.scripts },
    ].map((metric) => (
      <div
        key={metric.label}
        className="rounded-lg border border-white/10 p-3"
      >
        <p className="text-xs text-muted">{metric.label}</p>
        <p className="mt-1 text-xl font-semibold">{metric.value}</p>
      </div>
    ))}
  </div>

  <div className="mt-4 space-y-2 text-sm">
    <p>
      <span className="text-muted">JavaScript heuristic:</span>{' '}
      {result.modalities.html.features.suspiciousJavascript
        ? 'Potentially relevant indicators found'
        : 'No configured indicators found'}
    </p>
    <p>
      <span className="text-muted">External form submission:</span>{' '}
      {result.modalities.html.features.externalFormSubmission
        ? 'Detected'
        : 'Not detected'}
    </p>
  </div>
</div>

          </section>
        ) : null}

        {active === 'visual' ? (
          <>
            <WebsitePreview
              url={result.url}
              visual={visualFeatures}
              visualProbability={result.modalities.visual.probability}
              available={result.modalities.visual.available}
              ocrStatus={ocrStatus}
              ocrCharacterCount={ocrCharacterCount}
            />

            <section className="card p-5 sm:p-6">
              <h3 className="text-lg font-semibold">Visual evidence</h3>
              {visualFeatures.visualEvidence.length > 0 ? (
                <ul className="mt-4 list-disc space-y-2 pl-5 text-sm text-muted">
                  {visualFeatures.visualEvidence.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              ) : (
                <p className="mt-3 text-sm text-muted">
                  No additional visual evidence details were returned by the API.
                </p>
              )}
            </section>
          </>
        ) : null}

        {active === 'consistency' ? (
          <>
            <ConsistencyGraph
              scores={result.consistency}
              interpretation={result.summary}
            />
            <ConsistencyMatrix scores={result.consistency} />
            <IdentityAnalysis
              identities={result.identities}
              consistency={result.consistency}
            />
          </>
        ) : null}

        {active === 'explainability' ? (
          <>
            {result.explanation.top_features.length > 0 ? (
              <SHAPChart features={result.explanation.top_features} />
            ) : (
              <section className="card p-5 sm:p-6">
                <h3 className="text-lg font-semibold">Model Explainability</h3>
                <p className="mt-2 text-sm leading-6 text-muted">
                  Per-feature SHAP explanations are not currently available
                  for this live prediction. The following model probabilities
                  are available:
                </p>

                <ul className="mt-4 space-y-2 text-sm">
                  <li className="flex justify-between gap-4">
                    <span className="text-muted">URL model</span>
                    <span className="font-mono">
                      {(result.modalities.url.probability * 100).toFixed(2)}%
                    </span>
                  </li>
                  <li className="flex justify-between gap-4">
                    <span className="text-muted">HTML model</span>
                    <span className="font-mono">
                      {(result.modalities.html.probability * 100).toFixed(2)}%
                    </span>
                  </li>
                  <li className="flex justify-between gap-4">
                    <span className="text-muted">Visual model</span>
                    <span className="font-mono">
                      {(result.modalities.visual.probability * 100).toFixed(2)}%
                    </span>
                  </li>
                </ul>

                <p className="mt-4 text-xs leading-5 text-muted">
                  These are modality-level phishing probabilities, not feature
                  contributions and not percentages of the final prediction.
                </p>
              </section>
            )}
          </>
        ) : null}
      </div>
    </div>
  )
}
