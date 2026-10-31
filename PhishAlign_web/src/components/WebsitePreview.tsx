import { Eye, ImageOff } from 'lucide-react'
import type { VisualFeatures } from '../types/analysis'
import { Badge } from './Badge'

interface WebsitePreviewProps {
  url: string
  visual: VisualFeatures
  visualProbability: number
  available: boolean
  ocrStatus: string
  ocrCharacterCount: number
}

export function WebsitePreview({
  url,
  visual,
  visualProbability,
  available,
  ocrStatus,
  ocrCharacterCount,
}: WebsitePreviewProps) {
  const ocrCompleted =
    ocrStatus.toLowerCase() === 'ok' && ocrCharacterCount > 0

  const screenshotUrl = visual.screenshotUrl

  return (
    <section className="card p-5 sm:p-6">
      <h2 className="text-lg font-semibold">Captured Website Analysis</h2>
      <p className="mt-1 text-sm leading-6 text-muted">
        Screenshot captured for visual analysis. This is a static image of the
        analyzed page, not an interactive website.
      </p>

      <div className="mt-5 grid gap-6 lg:grid-cols-[1.4fr_1fr]">
        <div className="flex min-h-64 items-center justify-center overflow-hidden rounded-xl border border-white/10 bg-navy-950/50 p-3">
          {available && screenshotUrl ? (
            <img
              src={screenshotUrl}
              alt={`Captured screenshot of ${url}`}
              className="block max-h-[650px] w-full rounded-lg object-contain"
              loading="lazy"
              referrerPolicy="no-referrer"
            />
          ) : (
            <div className="flex flex-col items-center justify-center p-6 text-center">
              {available ? (
                <Eye className="h-9 w-9 text-cyan" aria-hidden />
              ) : (
                <ImageOff className="h-9 w-9 text-muted" aria-hidden />
              )}
              <p className="mt-3 font-medium text-ink">
                {available
                  ? 'Screenshot unavailable'
                  : 'Visual analysis unavailable'}
              </p>
              <p className="mt-2 max-w-sm text-sm leading-6 text-muted">
                {available
                  ? 'The API did not return a screenshot for this analysis.'
                  : 'No valid visual prediction is available for this page.'}
              </p>
            </div>
          )}
        </div>

        <div>
          <h3 className="text-sm font-semibold uppercase tracking-wide text-muted">
            Visual Model Output
          </h3>

          <dl className="mt-4 space-y-4 text-sm">
            <div>
              <dt className="text-muted">Analyzed URL</dt>
              <dd className="mt-1 break-all font-mono">{url}</dd>
            </div>

            <div className="flex items-center justify-between gap-3">
              <dt className="text-muted">Brand identification</dt>
              <dd>Not available</dd>
            </div>

            <div className="flex items-center justify-between gap-3">
              <dt className="text-muted">Credential form detection</dt>
              <dd>Not available</dd>
            </div>

            <div className="flex items-center justify-between gap-3">
              <dt className="text-muted">Visual phishing probability</dt>
              <dd className="font-mono">
                {(visualProbability * 100).toFixed(2)}%
              </dd>
            </div>

            <div>
              <dt className="text-muted">OCR status</dt>
              <dd className="mt-2 text-sm">
                {ocrCompleted
                  ? `OCR completed — ${ocrCharacterCount} characters extracted`
                  : `OCR unavailable or returned no text (${ocrStatus})`}
              </dd>
              <p className="mt-1 text-xs leading-5 text-muted">
                The API returns the OCR character count, not the extracted
                text itself.
              </p>
            </div>
          </dl>

          <div className="mt-5">
            <Badge tone="info">Model output, not identity verification</Badge>
          </div>
        </div>
      </div>
    </section>
  )
}