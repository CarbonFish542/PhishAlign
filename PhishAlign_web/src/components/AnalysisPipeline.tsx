
import { Check, Circle, LoaderCircle, X, Minus } from 'lucide-react'

export type StageStatus =
  | 'waiting'
  | 'processing'
  | 'completed'
  | 'failed'
  | 'skipped'

export interface PipelineStage {
  id: string
  label: string
}

interface AnalysisPipelineProps {
  stages: PipelineStage[]
  statuses: Record<string, StageStatus>
}

export const ANALYSIS_STAGES: PipelineStage[] = [
  { id: 'retrieved', label: 'URL Retrieved' },
  { id: 'html', label: 'HTML Extracted' },
  { id: 'screenshot', label: 'Screenshot Captured' },
  { id: 'url-model', label: 'URL Analysis' },
  { id: 'html-model', label: 'HTML Analysis' },
  { id: 'visual-model', label: 'Visual Analysis' },
  { id: 'consistency', label: 'Cross-Modal Consistency' },
  { id: 'explanation', label: 'Generating Explanation' },
]

export function AnalysisPipeline({ stages, statuses }: AnalysisPipelineProps) {
  const completed = stages.filter(
    (stage) => statuses[stage.id] === 'completed',
  ).length

  const failed = stages.some(
    (stage) => statuses[stage.id] === 'failed',
  )

  const progress = (completed / stages.length) * 100

  return (
    <div className="card p-6">
      <div className="mb-5 flex items-end justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-muted">
            Pipeline
          </p>
          <h2 className="mt-1 text-xl font-semibold">
            {failed ? 'Analysis Failed' : 'Analyzing Website'}
          </h2>
        </div>

        <p className="font-mono text-sm text-muted">
          {completed}/{stages.length} completed
        </p>
      </div>

      <div
        className="mb-6 h-1.5 overflow-hidden rounded-full bg-navy-950"
        role="progressbar"
        aria-label="Analysis pipeline progress"
        aria-valuemin={0}
        aria-valuemax={stages.length}
        aria-valuenow={completed}
      >
        <div
          className={`h-full transition-[width] duration-500 ${
            failed ? 'bg-risk' : 'bg-cyan'
          }`}
          style={{ width: `${progress}%` }}
        />
      </div>

      <ol className="space-y-3">
        {stages.map((stage) => {
          const status = statuses[stage.id] ?? 'waiting'

          return (
            <li key={stage.id} className="flex items-center gap-3 text-sm">
              {status === 'completed' ? (
                <span className="flex h-6 w-6 items-center justify-center rounded-full bg-safe/15 text-safe">
                  <Check className="h-3.5 w-3.5" aria-hidden />
                </span>
              ) : status === 'processing' ? (
                <span className="flex h-6 w-6 items-center justify-center rounded-full bg-cyan/15 text-cyan">
                  <LoaderCircle className="h-3.5 w-3.5 animate-spin" aria-hidden />
                </span>
              ) : status === 'failed' ? (
                <span className="flex h-6 w-6 items-center justify-center rounded-full bg-risk/15 text-risk">
                  <X className="h-3.5 w-3.5" aria-hidden />
                </span>
              ) : status === 'skipped' ? (
                <span className="flex h-6 w-6 items-center justify-center rounded-full bg-white/5 text-muted">
                  <Minus className="h-3.5 w-3.5" aria-hidden />
                </span>
              ) : (
                <span className="flex h-6 w-6 items-center justify-center rounded-full bg-white/5 text-muted">
                  <Circle className="h-3 w-3" aria-hidden />
                </span>
              )}

              <span
                className={
                  status === 'waiting' || status === 'skipped'
                    ? 'text-muted'
                    : status === 'failed'
                      ? 'text-risk'
                      : 'text-ink'
                }
              >
                {stage.label}
                {status === 'failed' ? ' — Failed' : ''}
                {status === 'skipped' ? ' — Skipped' : ''}
              </span>
            </li>
          )
        })}
      </ol>

      <p className="mt-5 text-xs leading-5 text-muted">
        Pipeline progress is illustrative. Individual stage completion is not
        independently reported by the backend.
      </p>
    </div>
  )
}
