import { Code2, Eye, Link2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { AnalysisTabs } from '../components/AnalysisTabs'
import { ModalityCard } from '../components/ModalityCard'
import { ResearchComparison } from '../components/ResearchComparison'
import { RiskScore } from '../components/RiskScore'
import { useAppState } from '../context/AppContext'

export function ResultsPage() {
  const navigate = useNavigate()
  const { result, researchMode } = useAppState()

  if (!result) {
    return (
      <div className="card mx-auto max-w-xl p-8 text-center">
        <h1 className="text-xl font-semibold">No analysis to display</h1>
        <p className="mt-2 text-sm text-muted">Run an analysis from the dashboard to see results.</p>
        <button
          type="button"
          onClick={() => navigate('/')}
          className="mt-5 rounded-xl bg-cyan px-4 py-2 text-sm font-semibold text-navy-950"
        >
          Go to dashboard
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-5 animate-fade-up">
      <RiskScore result={result} />

      <div className="grid gap-4 md:grid-cols-3">
        <ModalityCard
          icon={Link2}
          title="URL Model"
          probability={result.modalities.url.probability}
          explanation={result.modalities.url.explanation}
          available={result.modalities.url.available}
        />
        <ModalityCard
          icon={Code2}
          title="HTML Model"
          probability={result.modalities.html.probability}
          explanation={result.modalities.html.explanation}
          available={result.modalities.html.available}
        />
        <ModalityCard
          icon={Eye}
          title="Visual Model"
          probability={result.modalities.visual.probability}
          explanation={result.modalities.visual.explanation}
          available={result.modalities.visual.available}
        />
      </div>

      {researchMode ? <ResearchComparison result={result} /> : null}

      <AnalysisTabs result={result} />
    </div>
  )
}
