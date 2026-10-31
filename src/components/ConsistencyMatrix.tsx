
import type { ConsistencyScores } from '../types/analysis'

interface ConsistencyMatrixProps {
  scores: ConsistencyScores
}

function cellClass(value: number | null) {
  if (value === null) return 'text-muted bg-navy-950/40'
  if (value >= 0.7) return 'text-safe bg-safe/10'
  if (value >= 0.4) return 'text-warn bg-warn/10'
  return 'text-risk bg-risk/10'
}

function format(value: number | null) {
  return value === null
    ? 'Unavailable'
    : `${(value * 100).toFixed(1)}%`
}

export function ConsistencyMatrix({ scores }: ConsistencyMatrixProps) {
  const labels = ['URL', 'HTML', 'Screenshot'] as const

  const matrix: Array<Array<number | null>> = [
    [null, scores.url_html, scores.url_visual],
    [scores.url_html, null, scores.html_visual],
    [scores.url_visual, scores.html_visual, null],
  ]

  const domainRows = [
    {
      label: 'Domain ↔ HTML',
      value: scores.domain_html_available === false
        ? null
        : scores.domain_html ?? null,
    },
    {
      label: 'Domain ↔ Screenshot OCR',
      value: scores.domain_ocr_available === false
        ? null
        : scores.domain_ocr ?? null,
    },
    {
      label: 'Domain ↔ Page title',
      value: scores.domain_title_available === false
        ? null
        : scores.domain_title ?? null,
    },
  ]

  return (
    <section className="card p-5 sm:p-6">
      <div>
        <h3 className="text-lg font-semibold">Text-Overlap Matrix</h3>
        <p className="mt-1 max-w-xl text-sm text-muted">
          Pairwise Jaccard similarity between URL, HTML text, and screenshot OCR.
          These scores measure token overlap, not phishing probability.
        </p>
      </div>

      <div className="mt-5 overflow-x-auto">
        <table className="w-full min-w-[420px] border-collapse text-sm">
          <caption className="sr-only">
            Pairwise text-overlap scores
          </caption>
          <thead>
            <tr>
              <th className="p-2 text-left text-muted" />
              {labels.map((label) => (
                <th key={label} className="p-2 text-center font-medium text-muted">
                  {label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {labels.map((rowLabel, row) => (
              <tr key={rowLabel}>
                <th className="p-2 text-left font-medium text-muted">
                  {rowLabel}
                </th>
                {matrix[row].map((value, col) => (
                  <td
                    key={`${row}-${col}`}
                    className={`rounded-lg p-3 text-center font-mono ${cellClass(value)}`}
                  >
                    {format(value)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-8 border-t border-white/10 pt-5">
        <h4 className="font-semibold">Domain Identity Overlap</h4>
        <p className="mt-1 text-sm text-muted">
          Measures how much the domain's identity tokens overlap with page content.
          These comparisons are separate from the pairwise matrix above.
        </p>

        <div className="mt-4 space-y-3">
          {domainRows.map((item) => (
            <div
              key={item.label}
              className="flex items-center justify-between gap-4 rounded-xl bg-navy-950/40 p-4"
            >
              <span className="text-sm">{item.label}</span>
              <span
                className={`font-mono text-sm ${cellClass(item.value).split(' ')[0]}`}
              >
                {format(item.value)}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-5 flex flex-wrap gap-4 text-xs text-muted">
        <span className="inline-flex items-center gap-2">
          <span className="h-2.5 w-2.5 rounded-full bg-safe" />
          Higher overlap (≥70%)
        </span>
        <span className="inline-flex items-center gap-2">
          <span className="h-2.5 w-2.5 rounded-full bg-warn" />
          Moderate overlap (40–69%)
        </span>
        <span className="inline-flex items-center gap-2">
          <span className="h-2.5 w-2.5 rounded-full bg-risk" />
          Lower overlap (&lt;40%)
        </span>
      </div>
    </section>
  )
}
