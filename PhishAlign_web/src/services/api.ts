
import { AnalysisApiError } from '../types/analysis'
import type { AnalysisResult } from '../types/analysis'

const API_BASE_URL = 'http://127.0.0.1:8000'

interface BackendAnalysisResponse {
  requested_url: string
  final_url: string
  page_title: string

  html_metrics: {
    form_count: number
    password_fields: number
    external_links: number
    iframe_count: number
    script_count: number
    event_handler_attribute_count: number
    javascript_link_count: number
    suspicious_javascript_heuristic: boolean
    external_form_submission: boolean
  }

  http_status: number
  screenshot_data_url: string
  prediction: 'phishing' | 'legitimate'
  threshold: number
  phishalign_probability: number
  
  url_probability: number
  url_explanation: {
    available: boolean
    method: string
    output_space?: string
    base_value?: number
    top_features: {
      feature: string
      value: number
      contribution: number
      direction: 'increases_phishing_score' | 'decreases_phishing_score' | 'no_effect'
    }[]
  }
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
  html_metrics: {
  form_count: number
  password_fields: number
  external_links: number
  iframe_count: number
  script_count: number
  event_handler_attribute_count: number
  javascript_link_count: number
  suspicious_javascript_heuristic: boolean
  external_form_submission: boolean
}
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
    confidence: data.phishalign_probability,
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
          suspiciousTokens: [
            'login',
            'signin',
            'sign-in',
            'verify',
            'verification',
            'account',
            'secure',
            'security',
            'update',
            'password',
            'bank',
            'confirm',
            'billing',
            'wallet',
            'payment',
            'authenticate',
            'support',
            'recover',
            'webscr',
          ].filter((token) =>
  (data.final_url || data.requested_url).toLowerCase().includes(token),
),

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
          formCount: data.html_metrics.form_count,
          passwordFields: data.html_metrics.password_fields,
          externalLinks: data.html_metrics.external_links,
          iframes: data.html_metrics.iframe_count,
          scripts: data.html_metrics.script_count,
          suspiciousJavascript:
            data.html_metrics.suspicious_javascript_heuristic,
          externalFormSubmission:
            data.html_metrics.external_form_submission,
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
  top_features: data.url_explanation.available
    ? data.url_explanation.top_features.map((item) => ({
        name: item.feature,
        value: item.contribution,
      }))
    : [],
  narrative:
    'URL SHAP contributions explain the URL-only model score. They do not directly explain the final multimodal PhishAlign prediction.',
  modalityContributions: {
    url: 0,
    html: 0,
    visual: 0,
    consistency: 0,
  },
},


evidence: [
  ...(data.url_explanation.available
    ? data.url_explanation.top_features
        .filter((item) => item.contribution !== 0)
        .slice(0, 5)
        .map((item, index) => {
          const readableNames: Record<string, string> = {
            host_entropy: 'Host entropy',
            url_length: 'URL length',
            slash_count: 'Slash count',
            subdomain_count: 'Subdomain count',
            url_entropy: 'URL entropy',
            letter_count: 'Letter count',
            digit_count: 'Digit count',
            path_depth: 'Path depth',
            suspicious_token_count: 'Suspicious token count',
            hyphen_count: 'Hyphen count',
            host_length: 'Host length',
            path_length: 'Path length',
            query_length: 'Query length',
            fragment_length: 'Fragment length',
            dot_count: 'Dot count',
            at_count: '@ symbol count',
            question_count: 'Question mark count',
            equal_count: 'Equals sign count',
            ampersand_count: 'Ampersand count',
            percent_count: 'Percent sign count',
            underscore_count: 'Underscore count',
            uppercase_count: 'Uppercase letter count',
            special_char_count: 'Special character count',
            query_parameter_count: 'Query parameter count',
            https: 'HTTPS indicator',
            has_ip_address: 'IP address indicator',
            has_port: 'Port indicator',
            has_punycode: 'Punycode indicator',
            has_double_slash_in_path: 'Double slash in path',
            host_digit_count: 'Digits in hostname',
            path_digit_count: 'Digits in path',
          }

          const featureName =
            readableNames[item.feature] ??
            item.feature
              .replace(/_/g, ' ')
              .replace(/\b\w/g, (letter) => letter.toUpperCase())

          return {
            id: `url-shap-${index}`,
            impact: 'low' as const,
            category: 'URL model · SHAP',
            description:
              item.direction === 'increases_phishing_score'
                ? 'Pushes the URL model raw phishing score higher for this page.'
                : item.direction === 'decreases_phishing_score'
                  ? 'Pushes the URL model raw phishing score lower for this page.'
                  : 'Has no directional effect on the URL model raw score.',
            modality: 'url' as const,
            featureName,
            featureValue: item.value,
            contribution: item.contribution,
            direction: item.direction,
          }
        })
    : []),

  ...(data.html_metrics.password_fields > 0
    ? [
        {
          id: 'html-password-fields',
          impact: 'medium' as const,
          category: 'HTML structure',
          description: `The captured page contains ${data.html_metrics.password_fields} password field(s). Password fields are common on legitimate sites too, so this indicator alone does not establish phishing.`,
          modality: 'html' as const,
        },
      ]
    : []),

  ...(data.html_metrics.external_form_submission
    ? [
        {
          id: 'html-external-form',
          impact: 'medium' as const,
          category: 'HTML structure',
          description:
            'A form on the captured page submits to an external destination. This may be legitimate; review the destination and page context.',
          modality: 'html' as const,
        },
      ]
    : []),

  ...(data.html_metrics.suspicious_javascript_heuristic
    ? [
        {
          id: 'html-js-heuristic',
          impact: 'low' as const,
          category: 'HTML heuristic',
          description:
            'The configured JavaScript heuristic detected an indicator. This is a heuristic flag, not proof of malicious behavior.',
          modality: 'html' as const,
        },
      ]
    : []),
],
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
