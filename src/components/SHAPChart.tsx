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
    .sort((a, b) => Math.abs(b.value) - Math.abs(a.value))
    .map((feature) => ({
      name: feature.name,
      value: Number((feature.value * 100).toFixed(1)),
    }))

  return (
    <section className="card p-5 sm:p-6">
      <h3 className="text-lg font-semibold">Model Feature Contributions</h3>
      <p className="mt-1 text-sm text-muted">
        Feature contribution indicates how strongly each feature influenced the model prediction.
        Positive values contribute toward phishing; negative values contribute toward legitimate.
        These are not probabilities.
      </p>
      <div className="mt-6 h-[360px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ left: 16, right: 16, top: 8, bottom: 8 }}>
            <CartesianGrid stroke="rgba(255,255,255,0.06)" horizontal={false} />
            <XAxis type="number" stroke="#8b97ad" tick={{ fill: '#8b97ad', fontSize: 11 }} />
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
            />
            <ReferenceLine x={0} stroke="#8b97ad" />
            <Bar dataKey="value" radius={[4, 4, 4, 4]} maxBarSize={16}>
              {data.map((entry) => (
                <Cell key={entry.name} fill={entry.value >= 0 ? '#e5484d' : '#2fbf71'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}
