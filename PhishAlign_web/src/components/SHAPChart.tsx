
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import type { ShapFeature } from '../types/analysis'

interface SHAPChartProps {
  features: ShapFeature[]
}

export function SHAPChart({ features }: SHAPChartProps) {
  const data = [...features]
    .filter((feature) => typeof feature.contribution === 'number')
    .sort(
      (a, b) =>
        Math.abs(b.contribution ?? 0) - Math.abs(a.contribution ?? 0),
    )
    .map((feature) => ({
      name: feature.name,
      contribution: Number((feature.contribution ?? 0).toFixed(4)),
      featureValue: feature.value,
      direction: feature.direction,
    }))

  return (
    <section className="card p-5 sm:p-6">
      <h3 className="text-lg font-semibold">URL Model Feature Contributions</h3>
      <p className="mt-1 text-sm text-muted">
        SHAP TreeExplainer contributions for the URL XGBoost model. Positive
        values push the raw phishing score higher; negative values push it
        lower. These are raw-score contributions, not probabilities or
        percentage points.
      </p>

      {data.length === 0 ? (
        <p className="mt-4 text-sm text-muted">
          URL feature contributions are unavailable for this analysis.
        </p>
      ) : (
        <div className="mt-6 h-[360px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={data}
              layout="vertical"
              margin={{ left: 16, right: 24, top: 8, bottom: 8 }}
            >
              <CartesianGrid
                stroke="rgba(255,255,255,0.06)"
                horizontal={false}
              />
              <XAxis
                type="number"
                stroke="#8b97ad"
                tick={{ fill: '#8b97ad', fontSize: 11 }}
                tickFormatter={(value: number) => value.toFixed(2)}
              />
              <YAxis
                type="category"
                dataKey="name"
                width={170}
                stroke="#8b97ad"
                tick={{ fill: '#eef3fb', fontSize: 11 }}
              />
              <Tooltip
                cursor={{ fill: 'rgba(255,255,255,0.04)' }}
                contentStyle={{
                  background: '#131c2e',
                  border: '1px solid rgba(255,255,255,0.1)',
                  borderRadius: 12,
                }}
                formatter={(
                  value,
                  _name,
                  item,
                ) => {
                  const entry = item.payload
                  return [
                    `${Number(value).toFixed(4)} (raw score units)`,
                    `Contribution; input value: ${entry.featureValue}`,
                  ]
                }}
              />
              <ReferenceLine x={0} stroke="#8b97ad" />
              <Bar
                dataKey="contribution"
                name="SHAP contribution"
                radius={[4, 4, 4, 4]}
                maxBarSize={16}
              >
                {data.map((entry) => (
                  <Cell
                    key={entry.name}
                    fill={
                      entry.contribution > 0
                        ? '#e5484d'
                        : entry.contribution < 0
                          ? '#2fbf71'
                          : '#8b97ad'
                    }
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </section>
  )
}
