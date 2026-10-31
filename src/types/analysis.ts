export type Prediction = 'phishing' | 'legitimate' | 'suspicious'

export type ImpactLevel = 'high' | 'medium' | 'low'

export type ModalityKey = 'url' | 'html' | 'visual' | 'consistency' | 'fusion'

export type AnalysisErrorCode = 'UNAVAILABLE' | 'FAILED'

export interface EvidenceItem {
  id: string
  impact: ImpactLevel
  category: string
  description: string
  modality: ModalityKey
}

export interface UrlFeatures {
  fullUrl: string
  domain: string
  https: boolean
  length: number
  subdomainCount: number
  suspiciousTokens: string[]
  entropy: number
  specialCharacterCount: number
}

export interface HtmlFeatures {
  pageTitle: string
  formCount: number
  passwordFields: number
  externalLinks: number
  iframes: number
  scripts: number
  suspiciousJavascript: boolean
  externalFormSubmission: boolean
}

export interface VisualFeatures {
  screenshotUrl: string | null
  detectedBrand: string | null
  credentialFormDetected: boolean
  ocrText: string[]
  visualEvidence: string[]
}

export interface ModalityResult<TFeatures> {
  probability: number
  explanation: string
  features: TFeatures
  available: boolean
}


export interface ConsistencyScores {
  url_html: number
  url_visual: number
  html_visual: number

  // Domain identity overlap scores
  domain_html?: number | null
  domain_ocr?: number | null
  domain_title?: number | null

  // Whether each domain comparison could be performed
  domain_html_available?: boolean
  domain_ocr_available?: boolean
  domain_title_available?: boolean
}


export interface IdentityAnalysisData {
  url: string
  html: string
  visual: string
  conflict: boolean
  explanation: string
}

export interface ShapFeature {
  name: string
  value: number
}

export interface ResearchMetrics {
  accuracy: number
  precision: number
  recall: number
  f1: number
  rocAuc: number
}

export interface ResearchComparisonData {
  urlOnly: ResearchMetrics
  htmlOnly: ResearchMetrics
  visualOnly: ResearchMetrics
  conventionalMultimodal: ResearchMetrics
  proposedConsistencyAware: ResearchMetrics
  conventionalFusionProbability: number
  proposedProbability: number
}

export interface AnalysisResult {
  id: string
  url: string
  prediction: Prediction
  confidence: number
  summary: string
  modalities: {
    url: ModalityResult<UrlFeatures>
    html: ModalityResult<HtmlFeatures>
    visual: ModalityResult<VisualFeatures>
  }
  consistency: ConsistencyScores
  identities: IdentityAnalysisData
  explanation: {
    top_features: ShapFeature[]
    narrative: string
    modalityContributions: {
      url: number
      html: number
      visual: number
      consistency: number
    }
  }
  evidence: EvidenceItem[]
  research: ResearchComparisonData
}

export class AnalysisApiError extends Error {
  code: AnalysisErrorCode

  constructor(code: AnalysisErrorCode, message: string) {
    super(message)
    this.name = 'AnalysisApiError'
    this.code = code
  }
}
