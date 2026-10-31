import { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import {
  ANALYSIS_STAGES,
  AnalysisPipeline,
  type StageStatus,
} from '../components/AnalysisPipeline'
import { useAppState } from '../context/AppContext'
import { analyzeWebsite } from '../services/api'
import { AnalysisApiError } from '../types/analysis'

interface LocationState {
  url?: string
}

export function AnalyzePage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { submittedUrl, setSubmittedUrl, setResult } = useAppState()
  const url = (location.state as LocationState | null)?.url || submittedUrl
  const [statuses, setStatuses] = useState<Record<string, StageStatus>>(() =>
    Object.fromEntries(ANALYSIS_STAGES.map((stage) => [stage.id, 'waiting'])),
  )
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!url) {
      navigate('/', { replace: true })
    }
  }, [url, navigate])

  useEffect(() => {
    if (!url) return
    setSubmittedUrl(url)

    let cancelled = false
    const timers: number[] = []

    
async function run() {
  const startedAt = Date.now()
  let completedSuccessfully = false

  try {
    const resultPromise = analyzeWebsite(url)

    ANALYSIS_STAGES.forEach((stage, index) => {
      timers.push(
        window.setTimeout(() => {
          if (cancelled || completedSuccessfully) return

          setStatuses((current) => {
            // Do not restart stages already marked complete.
            if (
              current[stage.id] === 'completed' ||
              current[stage.id] === 'failed' ||
              current[stage.id] === 'skipped'
            ) {
              return current
            }

            return {
              ...current,
              [stage.id]: 'processing',
            }
          })
        }, index * 420),
      )
    })

    const result = await resultPromise

    const minDuration = ANALYSIS_STAGES.length * 420 + 500
    const remaining = Math.max(120, minDuration - (Date.now() - startedAt))

    await new Promise<void>((resolve) => {
      timers.push(window.setTimeout(resolve, remaining))
    })

    if (cancelled) return

    completedSuccessfully = true

    setStatuses(
      Object.fromEntries(
        ANALYSIS_STAGES.map((stage) => [stage.id, 'completed']),
      ),
    )

    setResult(result)
    navigate('/results', { replace: true })
  
} catch (caught) {
  if (cancelled) return

  timers.forEach((timer) => window.clearTimeout(timer))

  setStatuses(
    Object.fromEntries(
      ANALYSIS_STAGES.map((stage, index) => [
        stage.id,
        index === 0 ? 'failed' : 'skipped',
      ]),
    ),
  )

  if (caught instanceof AnalysisApiError) {
    setError(caught.message)
  } else {
    setError('Unable to analyze this website. Please try again.')
  }
}

}

    void run()

    return () => {
      cancelled = true
      timers.forEach((timer) => window.clearTimeout(timer))
    }
  }, [url, navigate, setResult, setSubmittedUrl])

  if (!url) return null

  return (
    <div className="mx-auto max-w-2xl animate-fade-up">
      <p className="text-xs font-semibold uppercase tracking-wide text-muted">Submitted URL</p>
      <p className="mt-2 break-all font-mono text-sm text-ink">{url}</p>
      <p className="mt-4 rounded-xl border border-warn/20 bg-warn/8 px-4 py-3 text-sm text-warn">
        PhishAlign is a research prototype. Do not enter sensitive credentials or personal information.
      </p>
      <div className="mt-6">
        <AnalysisPipeline stages={ANALYSIS_STAGES} statuses={statuses} />
      </div>
      {error ? (
        <div className="mt-6 rounded-xl border border-risk/25 bg-risk/10 p-4" role="alert">
          <p className="text-sm text-risk">{error}</p>
          <button
            type="button"
            onClick={() => navigate('/')}
            className="mt-3 text-sm font-medium text-ink underline"
          >
            Return to dashboard
          </button>
        </div>
      ) : null}
    </div>
  )
}
