import { Code2, GitCompare, Globe, Monitor } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { URLInput } from '../components/URLInput'
import { useAppState } from '../context/AppContext'
import { DEMO_URLS } from '../data/mockResults'

const includes = [
  { title: 'URL Analysis', text: 'Lexical and structural signals from the submitted address.', icon: Globe },
  { title: 'HTML Analysis', text: 'Page content, forms, scripts, and submission behavior.', icon: Code2 },
  { title: 'Visual Analysis', text: 'Screenshot appearance, brand cues, and OCR text.', icon: Monitor },
  { title: 'Cross-Modal Consistency', text: 'Whether URL, HTML, and visual identity agree.', icon: GitCompare },
]

export function HomePage() {
  const navigate = useNavigate()
  const { setSubmittedUrl, setResult } = useAppState()

  function startAnalysis(url: string) {
    setResult(null)
    setSubmittedUrl(url)
    navigate('/analyze', { state: { url } })
  }

  return (
    <div className="animate-fade-up">
      <section className="mx-auto max-w-3xl pt-4 text-center sm:pt-10">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan">Research prototype</p>
        <h1 className="mt-3 text-4xl font-semibold tracking-tight text-ink sm:text-5xl">
          Multimodal Phishing Detection
        </h1>
        <p className="mt-4 text-base leading-7 text-muted sm:text-lg">
          Analyze websites using URL, HTML, visual appearance, and cross-modal consistency.
        </p>
      </section>

      <div className="mx-auto mt-10 max-w-3xl">
        <div className="mb-3 flex flex-wrap items-center gap-2">
          <span className="text-xs text-muted">Demo scenarios</span>
          <button
            type="button"
            onClick={() => startAnalysis(DEMO_URLS.phishing)}
            className="rounded-full border border-risk/30 bg-risk/10 px-3 py-1 text-xs text-risk hover:bg-risk/15"
          >
            Phishing demo
          </button>
          <button
            type="button"
            onClick={() => startAnalysis(DEMO_URLS.legitimate)}
            className="rounded-full border border-safe/30 bg-safe/10 px-3 py-1 text-xs text-safe hover:bg-safe/15"
          >
            Legitimate demo
          </button>
        </div>
        <URLInput onSubmitUrl={startAnalysis} />
      </div>

      <section className="mx-auto mt-10 max-w-5xl">
        <p className="mb-4 text-center text-xs font-semibold uppercase tracking-wide text-muted">
          Analysis includes
        </p>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {includes.map((item, index) => {
            const Icon = item.icon
            return (
              <article key={item.title} className={`card animate-fade-up stagger-${index + 1} p-5 text-left`}>
                <Icon className="h-5 w-5 text-cyan" aria-hidden />
                <h2 className="mt-3 text-sm font-semibold">{item.title}</h2>
                <p className="mt-2 text-sm leading-6 text-muted">{item.text}</p>
              </article>
            )
          })}
        </div>
        <p className="mx-auto mt-8 max-w-3xl text-center text-sm leading-6 text-muted">
          PhishAlign analyzes multiple independent signals to identify phishing behavior and
          inconsistencies between webpage identity representations. This is a research prototype,
          not a production security product.
        </p>
      </section>
    </div>
  )
}
