export function normalizeUrl(input: string): string {
  const trimmed = input.trim()
  if (!trimmed) return ''
  if (/^[a-zA-Z][a-zA-Z\d+\-.]*:\/\//.test(trimmed)) {
    return trimmed
  }
  return `https://${trimmed}`
}

export function isValidWebsiteUrl(input: string): boolean {
  const candidate = normalizeUrl(input)
  if (!candidate) return false

  try {
    const parsed = new URL(candidate)
    if (!['http:', 'https:'].includes(parsed.protocol)) return false
    const host = parsed.hostname
    if (!host || host === 'localhost') return false
    if (!host.includes('.')) return false
    if (host.startsWith('.') || host.endsWith('.')) return false
    const labels = host.split('.')
    return labels.every((label) => label.length > 0 && /^[a-zA-Z0-9-]+$/.test(label))
  } catch {
    return false
  }
}
