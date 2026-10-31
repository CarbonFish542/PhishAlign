
import { AlertCircle, AlertTriangle, Info } from 'lucide-react'
import type { EvidenceItem } from '../types/analysis'
import { Badge } from './Badge'

interface EvidenceListProps {
  items: EvidenceItem[]
  title?: string
}

function getEvidenceIcon(category: string) {
  if (category.toLowerCase().includes('html')) return AlertTriangle
  if (category.toLowerCase().includes('shap')) return Info
  return AlertCircle
}

export function EvidenceList({
  items,
  title = 'Model evidence',
}: EvidenceListProps) {
  return (
    <section className="card p-4 sm:p-5">
      <h3 className="text-lg font-semibold">{title}</h3>

      <p className="mt-1 text-xs leading-5 text-muted">
        SHAP values explain contributions to the URL model score, not the final
        PhishAlign probability or a guarantee of website safety.
      </p>

      {items.length === 0 ? (
        <p className="mt-3 text-sm text-muted">
          No additional evidence was returned for this analysis.
        </p>
      ) : (
        <ul className="mt-3 space-y-2">
          {items.map((item) => {
            const Icon = getEvidenceIcon(item.category)
            const isShap = item.category.toLowerCase().includes('shap')
            const hasShapValues =
              item.featureName !== undefined &&
              typeof item.featureValue === 'number' &&
              typeof item.contribution === 'number'

            return (
              <li
                key={item.id}
                className="rounded-lg border border-white/6 bg-navy-950/40 p-3"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex min-w-0 items-center gap-2">
                    <Icon
                      className="h-4 w-4 shrink-0 text-muted"
                      aria-hidden
                    />
                    <p className="break-words text-sm font-medium text-ink">
                      {item.featureName ?? item.category}
                    </p>
                  </div>

                  <div className="flex flex-wrap gap-1.5">
                    <Badge>{item.modality.toUpperCase()}</Badge>
                    <Badge>
                      {isShap ? 'SHAP contribution' : 'Heuristic indicator'}
                    </Badge>
                  </div>
                </div>

                {hasShapValues ? (
                  <>
                    <div className="mt-2 flex flex-wrap items-center gap-x-5 gap-y-1 rounded-md bg-navy-900/70 px-3 py-2">
                      <p className="text-xs text-muted">
                        Feature value:{' '}
                        <span className="font-mono text-ink">
                          {item.featureValue!.toLocaleString(undefined, {
                            maximumFractionDigits: 4,
                          })}
                        </span>
                      </p>

                      <p className="text-xs text-muted">
                        SHAP:{' '}
                        <span
                          className={`font-mono font-semibold ${
                            item.contribution! > 0
                              ? 'text-risk'
                              : item.contribution! < 0
                                ? 'text-emerald-400'
                                : 'text-muted'
                          }`}
                        >
                          {item.contribution! > 0 ? '+' : ''}
                          {item.contribution!.toFixed(4)}
                        </span>
                      </p>
                    </div>

                    <p className="mt-2 text-xs leading-5 text-muted">
                      {item.description}
                    </p>
                  </>
                ) : (
                  <p className="mt-2 break-words text-sm leading-5 text-ink">
                    {item.description}
                  </p>
                )}
              </li>
            )
          })}
        </ul>
      )}
    </section>
  )
}
