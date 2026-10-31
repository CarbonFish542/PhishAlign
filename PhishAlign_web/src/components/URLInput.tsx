import { useMemo, useState, type FormEvent } from 'react'
import { Shield } from 'lucide-react'
import { isValidWebsiteUrl, normalizeUrl } from '../utils/url'

interface URLInputProps {
  initialValue?: string
  onSubmitUrl: (url: string) => void
  onChangeUrl?: (url: string) => void
}

export function URLInput({ initialValue = '', onSubmitUrl, onChangeUrl }: URLInputProps) {
  const [value, setValue] = useState(initialValue)

  const normalized = useMemo(() => normalizeUrl(value), [value])
  const valid = isValidWebsiteUrl(value)
  const showError = value.trim().length > 0 && !valid
  const disabled = !valid

  function handleChange(next: string) {
    setValue(next)
    onChangeUrl?.(next)
  }

  function handleSubmit(event: FormEvent) {
    event.preventDefault()
    if (!valid) return
    onSubmitUrl(normalized)
  }

  return (
    <form onSubmit={handleSubmit} className="card p-4 sm:p-6">
      <label htmlFor="website-url" className="mb-2 block text-sm font-medium text-ink">
        Website URL
      </label>
      <div className="flex flex-col gap-3 sm:flex-row">
        <input
          id="website-url"
          type="text"
          inputMode="url"
          autoComplete="url"
          placeholder="https://example.com"
          value={value}
          onChange={(event) => handleChange(event.target.value)}
          aria-invalid={showError}
          aria-describedby={showError ? 'url-error' : 'url-help'}
          className="h-12 flex-1 rounded-xl border border-white/10 bg-navy-950/70 px-4 text-sm text-ink outline-none ring-cyan/40 placeholder:text-muted/70 focus:border-cyan/40 focus:ring-2"
        />
        <button
          type="submit"
          disabled={disabled}
          className="inline-flex h-12 items-center justify-center gap-2 rounded-xl bg-cyan px-5 text-sm font-semibold text-navy-950 transition hover:bg-cyan/90 disabled:cursor-not-allowed disabled:bg-navy-600 disabled:text-muted"
        >
          <Shield className="h-4 w-4" aria-hidden />
          Analyze Website
        </button>
      </div>
      <p id="url-help" className="mt-2 text-xs text-muted">
        Enter a website URL… Protocol is added automatically if omitted.
      </p>
      {showError ? (
        <p id="url-error" className="mt-2 text-sm text-risk" role="alert">
          Please enter a valid website URL.
        </p>
      ) : null}
    </form>
  )
}
