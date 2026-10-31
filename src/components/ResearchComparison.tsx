
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import type { AnalysisResult } from '../types/analysis'
import { Badge } from './Badge'

interface ResearchComparisonProps {
  result: AnalysisResult
}

// Recorded official-test results, evaluated on 2,757 complete cases.
// These are benchmark metrics, not predictions for the submitted URL.
const TEST_BENCHMARK = {
  equalWeight: {
    accuracy: 95.43,
    precision: 98.46,
    recall: 91.41,
    f1: 94.81,
    rocAuc: 99.34,
  },
  probabilityOnly: {
    accuracy: 95.32,
    precision: 98.62,
    recall: 91.02,
    f1: 94.67,
    rocAuc: 99.36,
  },
  phishAlign: {
    accuracy: 96.34,
    precision: 99.40,
    recall: 92.53,
    f1: 95.84,
    rocAuc: 99.61,
  },
}

const chartData = [
  {
    name: 'Accuracy',
    equalWeight: TEST_BENCHMARK.equalWeight.accuracy,
    probabilityOnly: TEST_BENCHMARK.probabilityOnly.accuracy,
    phishAlign: TEST_BENCHMARK.phishAlign.accuracy,
  },
  {
    name: 'Precision',
    equalWeight: TEST_BENCHMARK.equalWeight.precision,
    probabilityOnly: TEST_BENCHMARK.probabilityOnly.precision,
    phishAlign: TEST_BENCHMARK.phishAlign.precision,
  },
  {
    name: 'Recall',
    equalWeight: TEST_BENCHMARK.equalWeight.recall,
    probabilityOnly: TEST_BENCHMARK.probabilityOnly.recall,
    phishAlign: TEST_BENCHMARK.phishAlign.recall,
  },
  {
    name: 'F1',
    equalWeight: TEST_BENCHMARK.equalWeight.f1,
    probabilityOnly: TEST_BENCHMARK.probabilityOnly.f1,
    phishAlign: TEST_BENCHMARK.phishAlign.f1,
  },
  {
    name: 'ROC-AUC',
    equalWeight: TEST_BENCHMARK.equalWeight.rocAuc,
    probabilityOnly: TEST_BENCHMARK.probabilityOnly.rocAuc,
    phishAlign: TEST_BENCHMARK.phishAlign.rocAuc,
  },
]

export function ResearchComparison({ result }: ResearchComparisonProps) {
  const f1Improvement =
    TEST_BENCHMARK.phishAlign.f1 - TEST_BENCHMARK.equalWeight.f1

  const aucImprovement =
    TEST_BENCHMARK.phishAlign.rocAuc - TEST_BENCHMARK.equalWeight.rocAuc

  return (
    <section className="card p-5 sm:p-6">
      <div className="flex flex-wrap items-center gap-2">
        <h3 className="text-lg font-semibold">Research Comparison</h3>
        <Badge tone="info">Official Test Benchmark</Badge>
      </div>

      <p className="mt-2 text-sm leading-6 text-muted">
        Dataset-level performance comparison using the recorded official
        test-set evaluation. These metrics are independent of the website
        currently being analyzed.
      </p>

      <div className="mt-6 grid gap-4 sm:grid-cols-3">
        <div className="rounded-xl bg-navy-950/50 p-4">
          <p className="text-xs uppercase tracking-wide text-muted">
            Live Modality Probabilities
          </p>
          <ul className="mt-3 space-y-2 font-mono text-sm">
            <li className="flex justify-between gap-3">
              <span>URL</span>
              <span>{(result.modalities.url.probability * 100).toFixed(2)}%</span>
            </li>
            <li className="flex justify-between gap-3">
              <span>HTML</span>
              <span>{(result.modalities.html.probability * 100).toFixed(2)}%</span>
            </li>
            <li className="flex justify-between gap-3">
              <span>Visual</span>
              <span>{(result.modalities.visual.probability * 100).toFixed(2)}%</span>
            </li>
          </ul>
          <p className="mt-3 text-xs leading-5 text-muted">
            Phishing probabilities for this website only.
          </p>
        </div>

        <div className="rounded-xl bg-navy-950/50 p-4">
          <p className="text-xs uppercase tracking-wide text-muted">
            Equal-Weight Fusion
          </p>
          <p className="mt-3 text-sm text-muted">
            Official-test F1 score
          </p>
          <p className="mt-2 font-mono text-3xl">
            {TEST_BENCHMARK.equalWeight.f1.toFixed(2)}%
          </p>
          <p className="mt-3 text-sm text-muted">
            Live phishing probability
          </p>
          <p className="mt-1 font-mono text-xl">
            {(result.research.conventionalFusionProbability * 100).toFixed(2)}%
          </p>
        </div>

        <div className="rounded-xl border border-cyan/20 bg-cyan/5 p-4">
          <p className="text-xs uppercase tracking-wide text-cyan">
            Proposed PhishAlign
          </p>
          <p className="mt-3 text-sm text-muted">
            Official-test F1 score
          </p>
          <p className="mt-2 font-mono text-3xl text-ink">
            {TEST_BENCHMARK.phishAlign.f1.toFixed(2)}%
          </p>
          <p className="mt-3 text-sm text-muted">
            Live phishing probability
          </p>
          <p className="mt-1 font-mono text-xl">
            {(result.research.proposedProbability * 100).toFixed(2)}%
          </p>
          <p className="mt-3 text-sm text-safe">
            F1 improvement: +{f1Improvement.toFixed(2)} percentage points
          </p>
          <p className="mt-1 text-sm text-safe">
            ROC-AUC improvement: +{aucImprovement.toFixed(2)} percentage points
          </p>
        </div>
      </div>

      <div className="mt-8">
        <h4 className="font-semibold">Official Test-Set Performance</h4>
        <p className="mt-1 text-sm text-muted">
          Metrics are percentages. Higher is better for all five measures.
        </p>
      </div>

      <div className="mt-4 h-[340px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            margin={{ top: 8, right: 8, left: 0, bottom: 8 }}
          >
            <CartesianGrid stroke="rgba(255,255,255,0.06)" vertical={false} />
            <XAxis
              dataKey="name"
              stroke="#8b97ad"
              tick={{ fill: '#8b97ad', fontSize: 12 }}
            />
            <YAxis
              stroke="#8b97ad"
              tick={{ fill: '#8b97ad', fontSize: 11 }}
              domain={[90, 100]}
              tickFormatter={(value: number) => `${value}%`}
            />
            <Tooltip
              formatter={(value) =>
                typeof value === 'number' ? `${value.toFixed(2)}%` : value
              }
              contentStyle={{
                background: '#131c2e',
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: 12,
              }}
            />
            <Legend />
            <Bar
              dataKey="equalWeight"
              name="Equal-weight fusion"
              fill="#e8a838"
              radius={4}
            />
            <Bar
              dataKey="probabilityOnly"
              name="Probability-only stacking"
              fill="#4aa8e8"
              radius={4}
            />
            <Bar
              dataKey="phishAlign"
              name="PhishAlign"
              fill="#2fbf71"
              radius={4}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-5 rounded-xl bg-navy-950/40 p-4 text-sm leading-6 text-muted">
        <p>
          <strong className="text-ink">Evaluation coverage:</strong> 2,757 of
          2,771 official test samples (99.49%). Fourteen samples were excluded
          from the complete-case comparison.
        </p>
        <p className="mt-2">
          PhishAlign achieved an F1 score of 95.84% versus 94.81% for
          equal-weight fusion, an improvement of 1.03 percentage points.
          Group-bootstrap confidence intervals for the recorded F1 and
          ROC-AUC improvements were above zero.
        </p>
      </div>
    </section>
  )
}
