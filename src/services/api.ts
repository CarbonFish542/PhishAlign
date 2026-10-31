
import { AnalysisApiError } from '../types/analysis'
import type { AnalysisResult } from '../types/analysis'

const API_BASE_URL = 'http://127.0.0.1:8000'

interface BackendAnalysisResponse {
  requested_url: string
  final_url: string
  page_title: string
  http_status: number
  screenshot_data_url: string
  prediction: 'phishing' | 'legitimate'
  threshold: number
  phishalign_probability: number
  url_probability: number
  html_probability: number
  visual_probability: number
  equal_weight_probability: number
  probability_only_probability: number
  ocr_status: string
  ocr_character_count: number
  ocr_error: string
  consistency_features: Record<string, number | boolean>
  modality_predictions: {
    url: {
      phishing_probability: number
      features: Record<string, unknown>
    }
    html: { phishing_probability: number }
    visual: { phishing_probability: number }
  }
}

export async function analyzeWebsite(url: string): Promise<AnalysisResult> {
  let response: Response

  try {
    response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: url.trim() }),
    })
  } catch {
    throw new AnalysisApiError(
      'UNAVAILABLE',
      'Cannot connect to the PhishAlign backend. Check that the API is running on port 8000.',
    )
  }

  if (!response.ok) {
    let detail = 'Unable to analyze this website. Please try again.'

    try {
      const body = await response.json()
      if (typeof body.detail === 'string') detail = body.detail
    } catch {
      // Keep the fallback message if the response is not JSON.
    }

    throw new AnalysisApiError(
      response.status === 400 ? 'UNAVAILABLE' : 'FAILED',
      detail,
    )
  }

  const data = (await response.json()) as BackendAnalysisResponse

  // The existing UI expects a richer result than the API currently provides.
  // Do not invent SHAP values, detected brands, or HTML element counts.
  // These compatibility fields are placeholders until the UI is adapted.
  const features = data.modality_predictions.url.features
  const host = (() => {
    try {
      return new URL(data.final_url).hostname
    } catch {
      return data.final_url
    }
  })()

  const numericFeature = (key: string, fallback = 0): number => {
    const value = features[key]
    return typeof value === 'number' && Number.isFinite(value)
      ? value
      : fallback
  }

  const phishing = data.prediction === 'phishing'
  const urlProbability = data.url_probability
  const htmlProbability = data.html_probability
  const visualProbability = data.visual_probability

  const consistency = data.consistency_features
  const score = (key: string): number => {
    const value = consistency[key]
    return typeof value === 'number' && Number.isFinite(value) ? value : 0
  }

  const result = {
    id: crypto.randomUUID(),
    url: data.final_url || data.requested_url,
    prediction: data.prediction,
    confidence: phishing
      ? data.phishalign_probability
      : 1 - data.phishalign_probability,
    summary: `PhishAlign classified this page as ${data.prediction}. Phishing probability: ${(data.phishalign_probability * 100).toFixed(2)}%. HTTP status: ${data.http_status}.`,
    modalities: {
      url: {
        probability: urlProbability,
        explanation: 'Probability predicted by the URL-only XGBoost model.',
        available: true,
        features: {
          fullUrl: data.final_url || data.requested_url,
          domain: host,
          https: (data.final_url || data.requested_url).startsWith('https://'),
          length: numericFeature('url_length', (data.final_url || data.requested_url).length),
          subdomainCount: numericFeature('subdomain_count'),
          suspiciousTokens: [],
          entropy: numericFeature('url_entropy'),
          specialCharacterCount: numericFeature('special_character_count'),
        },
      },
      html: {
        probability: htmlProbability,
        explanation: 'Probability predicted by the HTML-only XGBoost model.',
        available: true,
        features: {
          pageTitle: data.page_title || 'Not available',
          formCount: 0,
          passwordFields: 0,
          externalLinks: 0,
          iframes: 0,
          scripts: 0,
          suspiciousJavascript: false,
          externalFormSubmission: false,
        },
      },
      visual: {
        probability: visualProbability,
        explanation: 'Probability predicted by the screenshot MobileNetV3-Small model.',
        available: true,
        features: {
          screenshotUrl: data.screenshot_data_url,
          detectedBrand: null,
          credentialFormDetected: false,
          ocrText: [],
          visualEvidence: [
            `OCR status: ${data.ocr_status}`,
            `OCR characters extracted: ${data.ocr_character_count}`,
          ],
        },
      },
    },
    

consistency: {
  url_html: score('url_html_jaccard'),
  url_visual: score('url_ocr_jaccard'),
  html_visual: score('html_ocr_jaccard'),

  domain_html: consistency.domain_html_jaccard_v3 == null
    ? null
    : score('domain_html_jaccard_v3'),

  domain_ocr: consistency.domain_ocr_jaccard_v3 == null
    ? null
    : score('domain_ocr_jaccard_v3'),

  domain_title: consistency.domain_title_jaccard_v3 == null
    ? null
    : score('domain_title_jaccard_v3'),

  domain_html_available: score('domain_html_comparison_available_v3') === 1,
  domain_ocr_available: score('domain_ocr_comparison_available_v3') === 1,
  domain_title_available: score('domain_title_comparison_available_v3') === 1,
},


    identities: {
  url: host,
  html: data.page_title || 'Page title unavailable',
  visual:
    data.ocr_status.toLowerCase() === 'ok' && data.ocr_character_count > 0
      ? `OCR completed — ${data.ocr_character_count} characters extracted`
      : `OCR unavailable or returned no text (${data.ocr_status})`,
  conflict: false,
  explanation:
    'Identity conflict is not inferred from these labels alone. Review the detailed consistency features.',
},
explanation: {
  top_features: [],
  narrative: 'Per-feature attribution is not currently returned by the inference API.',
  modalityContributions: {
    url: 0,
    html: 0,
    visual: 0,
    consistency: 0,
  },
},
    evidence: [],
    research: {
      urlOnly: { accuracy: 0, precision: 0, recall: 0, f1: 0, rocAuc: 0 },
      htmlOnly: { accuracy: 0, precision: 0, recall: 0, f1: 0, rocAuc: 0 },
      visualOnly: { accuracy: 0, precision: 0, recall: 0, f1: 0, rocAuc: 0 },
      conventionalMultimodal: { accuracy: 0, precision: 0, recall: 0, f1: 0, rocAuc: 0 },
      proposedConsistencyAware: { accuracy: 0, precision: 0, recall: 0, f1: 0, rocAuc: 0 },
      conventionalFusionProbability: data.equal_weight_probability,
      proposedProbability: data.phishalign_probability,
    },
  } satisfies AnalysisResult

  return result
}

export async function getAnalysisResult(_id: string): Promise<AnalysisResult> {
  throw new AnalysisApiError(
    'FAILED',
    'Saved analysis lookup is not available with the live API yet.',
  )
}
