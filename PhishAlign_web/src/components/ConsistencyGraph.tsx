import type { ConsistencyScores } from '../types/analysis'

interface ConsistencyGraphProps {
  scores: ConsistencyScores
  interpretation: string
}

function consistencyTone(value: number): string {
  if (value >= 0.7) return '#2fbf71'
  if (value >= 0.4) return '#e8a838'
  return '#e5484d'
}

function pct(value: number) {
  return `${Math.round(value * 100)}%`
}

export function ConsistencyGraph({ scores, interpretation }: ConsistencyGraphProps) {

const pairs = [
  { label: 'URL–HTML text overlap (Jaccard)', value: scores.url_html },
  { label: 'URL–OCR text overlap (Jaccard)', value: scores.url_visual },
  { label: 'HTML–OCR text overlap (Jaccard)', value: scores.html_visual },
]


  return (
    <section className="card p-5 sm:p-6">
      <h2 className="text-xl font-semibold">Cross-Modal Text Overlap</h2>
      
<p className="mt-2 max-w-2xl text-sm leading-6 text-muted">
  These indicators measure token overlap between the URL, HTML text,
  and screenshot OCR. Low overlap alone does not prove phishing, and
  these values are not calibrated probabilities.
</p>


      <div className="mt-6 grid gap-8 lg:grid-cols-[1.2fr_1fr]">
        <div className="overflow-x-auto">
          <svg viewBox="0 0 420 300" className="mx-auto h-auto w-full max-w-lg" role="img" aria-label="Text overlap measurements between URL, HTML and screenshot OCR">
            <line x1="80" y1="70" x2="340" y2="70" stroke={consistencyTone(scores.url_html)} strokeWidth="3" />
            <line x1="80" y1="70" x2="210" y2="230" stroke={consistencyTone(scores.url_visual)} strokeWidth="3" />
            <line x1="340" y1="70" x2="210" y2="230" stroke={consistencyTone(scores.html_visual)} strokeWidth="3" />

            <circle cx="80" cy="70" r="22" fill="#1c2840" stroke="#4aa8e8" strokeWidth="2" />
            <circle cx="340" cy="70" r="22" fill="#1c2840" stroke="#4aa8e8" strokeWidth="2" />
            <circle cx="210" cy="230" r="22" fill="#1c2840" stroke="#4aa8e8" strokeWidth="2" />

            <text x="80" y="34" textAnchor="middle" fill="#eef3fb" fontSize="13">URL</text>
            <text x="340" y="34" textAnchor="middle" fill="#eef3fb" fontSize="13">HTML</text>
            <text x="210" y="274" textAnchor="middle" fill="#eef3fb" fontSize="13">SCREENSHOT</text>

            <text x="210" y="60" textAnchor="middle" fill={consistencyTone(scores.url_html)} fontSize="13" fontFamily="IBM Plex Mono">
              {pct(scores.url_html)}
            </text>
            <text x="110" y="160" fill={consistencyTone(scores.url_visual)} fontSize="13" fontFamily="IBM Plex Mono">
              {pct(scores.url_visual)}
            </text>
            <text x="286" y="160" fill={consistencyTone(scores.html_visual)} fontSize="13" fontFamily="IBM Plex Mono">
              {pct(scores.html_visual)}
            </text>
          </svg>
        </div>

        <div className="space-y-3">
          {pairs.map((pair) => (
            <div key={pair.label} className="rounded-xl border border-white/6 bg-navy-950/40 p-4">
              <div className="flex items-center justify-between">
                <p className="text-sm text-ink">{pair.label}</p>
                <p className="font-mono text-lg" style={{ color: consistencyTone(pair.value) }}>
                  {pct(pair.value)}
                </p>
              </div>
            </div>
          ))}
          <p className="pt-2 text-sm leading-6 text-ink/90">{interpretation}</p>
        </div>
      </div>
    </section>
  )
}
