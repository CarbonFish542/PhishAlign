import { ArrowDown, GitCompare } from 'lucide-react'

export function AboutPage() {
  return (
    <div className="mx-auto max-w-3xl space-y-6 animate-fade-up">
      <header>
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-cyan">Methodology</p>
        <h1 className="mt-2 text-3xl font-semibold">About PhishAlign</h1>
        <p className="mt-3 text-sm leading-7 text-muted">
          PhishAlign is a final-year engineering research prototype for phishing website detection
          using URL, HTML, and screenshot modalities, with explicit cross-modal consistency analysis.
        </p>
      </header>

      <section className="card p-6">
        <h2 className="text-lg font-semibold">Problem</h2>
        <p className="mt-3 text-sm leading-7 text-muted">
          Phishing websites can imitate legitimate brands while using unrelated or suspicious
          domains and webpage structures. A page can look like Microsoft, read like Microsoft, and
          still live on a domain that has nothing to do with Microsoft.
        </p>
      </section>

      <section className="card p-6">
        <h2 className="text-lg font-semibold">Proposed Approach</h2>
        <p className="mt-3 text-sm leading-7 text-muted">
          PhishAlign analyzes URL + HTML + Screenshot and explicitly evaluates cross-modal
          consistency: whether the three representations of website identity tell the same story.
        </p>
      </section>

      <section className="card p-6">
        <h2 className="text-lg font-semibold">Architecture</h2>
        <div className="mt-5 grid gap-3 sm:grid-cols-3">
          <ArchBox title="URL" subtitle="URL Model" />
          <ArchBox title="HTML" subtitle="HTML Model" />
          <ArchBox title="Screenshot" subtitle="Visual Model" />
        </div>
        <div className="my-4 flex justify-center text-muted">
          <ArrowDown className="h-5 w-5" aria-hidden />
        </div>
        <div className="grid gap-3 sm:grid-cols-3">
          <ArchBox title="URL ↔ HTML" subtitle="Consistency" />
          <ArchBox title="URL ↔ Screenshot" subtitle="Consistency" />
          <ArchBox title="HTML ↔ Screenshot" subtitle="Consistency" />
        </div>
        <div className="my-4 flex justify-center text-muted">
          <GitCompare className="h-5 w-5" aria-hidden />
        </div>
        <div className="space-y-3 text-center">
          <ArchBox title="Consistency Features" subtitle="Fusion representation" />
          <ArrowDown className="mx-auto h-5 w-5 text-muted" aria-hidden />
          <ArchBox title="Final Classifier" subtitle="Phishing / Legitimate" />
        </div>
      </section>

      <section className="card p-6">
        <h2 className="text-lg font-semibold">Explainability</h2>
        <p className="mt-3 text-sm leading-7 text-muted">
          SHAP is used to identify influential features after a prediction is produced. Feature
          contributions show direction and relative influence; they are not probabilities and are
          not claimed to be calibrated.
        </p>
      </section>

      <section className="card p-6">
        <h2 className="text-lg font-semibold">Research Question</h2>
        <p className="mt-3 text-sm leading-7 text-ink">
          Can explicit cross-modal consistency between URL, HTML content, and webpage appearance
          improve phishing website detection compared with conventional multimodal fusion?
        </p>
      </section>
    </div>
  )
}

function ArchBox({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div className="rounded-xl border border-white/8 bg-navy-950/50 px-4 py-3">
      <p className="text-sm font-medium">{title}</p>
      <p className="text-xs text-muted">{subtitle}</p>
    </div>
  )
}
