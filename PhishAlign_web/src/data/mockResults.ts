import type { AnalysisResult } from '../types/analysis'

const phishingResearch = {
  urlOnly: { accuracy: 0.812, precision: 0.794, recall: 0.768, f1: 0.781, rocAuc: 0.861 },
  htmlOnly: { accuracy: 0.847, precision: 0.831, recall: 0.822, f1: 0.826, rocAuc: 0.892 },
  visualOnly: { accuracy: 0.869, precision: 0.858, recall: 0.841, f1: 0.849, rocAuc: 0.911 },
  conventionalMultimodal: { accuracy: 0.918, precision: 0.907, recall: 0.901, f1: 0.904, rocAuc: 0.954 },
  proposedConsistencyAware: { accuracy: 0.967, precision: 0.961, recall: 0.952, f1: 0.956, rocAuc: 0.983 },
  conventionalFusionProbability: 0.918,
  proposedProbability: 0.967,
}

const legitimateResearch = {
  urlOnly: { accuracy: 0.812, precision: 0.794, recall: 0.768, f1: 0.781, rocAuc: 0.861 },
  htmlOnly: { accuracy: 0.847, precision: 0.831, recall: 0.822, f1: 0.826, rocAuc: 0.892 },
  visualOnly: { accuracy: 0.869, precision: 0.858, recall: 0.841, f1: 0.849, rocAuc: 0.911 },
  conventionalMultimodal: { accuracy: 0.918, precision: 0.907, recall: 0.901, f1: 0.904, rocAuc: 0.954 },
  proposedConsistencyAware: { accuracy: 0.967, precision: 0.961, recall: 0.952, f1: 0.956, rocAuc: 0.983 },
  conventionalFusionProbability: 0.933,
  proposedProbability: 0.982,
}

export const DEMO_URLS = {
  phishing: 'https://secure-microsoft-login-example.xyz/verify',
  legitimate: 'https://www.microsoft.com/',
  unavailable: 'https://unavailable.example',
  failed: 'https://fail-analyze.example',
} as const

export const phishingResult: AnalysisResult = {
  id: 'demo-phishing',
  url: DEMO_URLS.phishing,
  prediction: 'phishing',
  confidence: 0.967,
  summary:
    'Strong inconsistency detected between the URL identity and the visual webpage identity.',
  modalities: {
    url: {
      probability: 0.873,
      explanation: 'Suspicious URL characteristics detected',
      available: true,
      features: {
        fullUrl: DEMO_URLS.phishing,
        domain: 'secure-microsoft-login-example.xyz',
        https: true,
        length: 50,
        subdomainCount: 0,
        suspiciousTokens: ['secure', 'login', 'verify', 'microsoft'],
        entropy: 4.21,
        specialCharacterCount: 3,
      },
    },
    html: {
      probability: 0.912,
      explanation: 'Credential form and suspicious page content detected',
      available: true,
      features: {
        pageTitle: 'Sign in to your Microsoft account',
        formCount: 1,
        passwordFields: 1,
        externalLinks: 4,
        iframes: 0,
        scripts: 6,
        suspiciousJavascript: true,
        externalFormSubmission: true,
      },
    },
    visual: {
      probability: 0.941,
      explanation: 'Visual similarity to a known brand login page detected',
      available: true,
      features: {
        screenshotUrl: null,
        detectedBrand: 'Microsoft',
        credentialFormDetected: true,
        ocrText: ['Microsoft', 'Sign in', 'Password', 'Verify your account'],
        visualEvidence: [
          'Layout matches a known Microsoft account login page',
          'Brand marks and color palette closely imitate official sign-in UI',
          'Prominent password and verification fields',
        ],
      },
    },
  },
  consistency: {
    url_html: 0.31,
    url_visual: 0.18,
    html_visual: 0.91,
  },
  identities: {
    url: 'Unknown / Suspicious',
    html: 'Microsoft',
    visual: 'Microsoft',
    conflict: true,
    explanation:
      'The HTML and visual appearance indicate Microsoft, while the submitted domain does not correspond to the detected identity.',
  },
  explanation: {
    narrative:
      'The page looks and reads like a Microsoft sign-in experience, but the domain is unrelated. Cross-modal disagreement between URL identity and the HTML/visual identity is the dominant phishing signal.',
    top_features: [
      { name: 'Domain-brand mismatch', value: 0.28 },
      { name: 'URL ↔ Screenshot inconsistency', value: 0.24 },
      { name: 'Password field detected', value: 0.16 },
      { name: 'External form submission', value: 0.14 },
      { name: 'URL contains "verify"', value: 0.11 },
      { name: 'HTML visual similarity', value: 0.09 },
      { name: 'Suspicious JavaScript', value: 0.07 },
      { name: 'HTTPS present', value: -0.04 },
      { name: 'URL length', value: 0.05 },
    ],
    modalityContributions: {
      url: 0.22,
      html: 0.26,
      visual: 0.24,
      consistency: 0.28,
    },
  },
  evidence: [
    {
      id: 'e1',
      impact: 'high',
      category: 'Identity mismatch',
      description: 'Domain does not match detected webpage brand',
      modality: 'consistency',
    },
    {
      id: 'e2',
      impact: 'high',
      category: 'Content',
      description: 'Suspicious login/verification keywords',
      modality: 'url',
    },
    {
      id: 'e3',
      impact: 'high',
      category: 'Form behavior',
      description: 'External credential submission detected',
      modality: 'html',
    },
    {
      id: 'e4',
      impact: 'high',
      category: 'Cross-modal',
      description: 'URL ↔ Screenshot inconsistency is high',
      modality: 'consistency',
    },
    {
      id: 'e5',
      impact: 'medium',
      category: 'URL structure',
      description: 'Brand tokens embedded in an unrelated domain',
      modality: 'url',
    },
    {
      id: 'e6',
      impact: 'medium',
      category: 'Scripts',
      description: 'Suspicious JavaScript behavior',
      modality: 'html',
    },
    {
      id: 'e7',
      impact: 'low',
      category: 'Lexical',
      description: 'Multiple special characters in URL',
      modality: 'url',
    },
  ],
  research: phishingResearch,
}

export const legitimateResult: AnalysisResult = {
  id: 'demo-legitimate',
  url: DEMO_URLS.legitimate,
  prediction: 'legitimate',
  confidence: 0.982,
  summary: 'URL, HTML content, and visual identity are aligned with the Microsoft brand.',
  modalities: {
    url: {
      probability: 0.031,
      explanation: 'Official domain structure with no suspicious lexical cues',
      available: true,
      features: {
        fullUrl: DEMO_URLS.legitimate,
        domain: 'www.microsoft.com',
        https: true,
        length: 24,
        subdomainCount: 1,
        suspiciousTokens: [],
        entropy: 3.12,
        specialCharacterCount: 0,
      },
    },
    html: {
      probability: 0.028,
      explanation: 'Page structure matches an official brand homepage',
      available: true,
      features: {
        pageTitle: 'Microsoft – Cloud, Computers, Apps & Gaming',
        formCount: 1,
        passwordFields: 0,
        externalLinks: 18,
        iframes: 1,
        scripts: 12,
        suspiciousJavascript: false,
        externalFormSubmission: false,
      },
    },
    visual: {
      probability: 0.047,
      explanation: 'Visual layout consistent with the official Microsoft site',
      available: true,
      features: {
        screenshotUrl: null,
        detectedBrand: 'Microsoft',
        credentialFormDetected: false,
        ocrText: ['Microsoft', 'Products', 'Search', 'Sign in'],
        visualEvidence: [
          'Official homepage composition and navigation',
          'Brand marks match known Microsoft assets',
          'No credential harvesting layout detected',
        ],
      },
    },
  },
  consistency: {
    url_html: 0.96,
    url_visual: 0.94,
    html_visual: 0.97,
  },
  identities: {
    url: 'Microsoft',
    html: 'Microsoft',
    visual: 'Microsoft',
    conflict: false,
    explanation:
      'The submitted domain, HTML content, and visual appearance all correspond to Microsoft. No identity conflict was detected.',
  },
  explanation: {
    narrative:
      'All three modalities agree on a Microsoft identity, and none of the high-impact phishing cues are present. Consistency features further reduce the phishing score relative to conventional fusion.',
    top_features: [
      { name: 'Official domain match', value: -0.31 },
      { name: 'URL ↔ HTML consistency', value: -0.22 },
      { name: 'HTML ↔ Screenshot consistency', value: -0.18 },
      { name: 'Known brand homepage layout', value: -0.14 },
      { name: 'No password field', value: -0.11 },
      { name: 'HTTPS present', value: -0.06 },
      { name: 'External form submission', value: -0.05 },
      { name: 'URL length', value: -0.02 },
    ],
    modalityContributions: {
      url: 0.18,
      html: 0.21,
      visual: 0.19,
      consistency: 0.42,
    },
  },
  evidence: [
    {
      id: 'l1',
      impact: 'high',
      category: 'Identity alignment',
      description: 'Domain matches the detected Microsoft brand',
      modality: 'consistency',
    },
    {
      id: 'l2',
      impact: 'high',
      category: 'Cross-modal',
      description: 'High agreement across URL, HTML, and screenshot identities',
      modality: 'consistency',
    },
    {
      id: 'l3',
      impact: 'medium',
      category: 'Content',
      description: 'No credential harvesting form pattern detected',
      modality: 'html',
    },
    {
      id: 'l4',
      impact: 'medium',
      category: 'Visual',
      description: 'Homepage layout rather than a cloned login page',
      modality: 'visual',
    },
    {
      id: 'l5',
      impact: 'low',
      category: 'Lexical',
      description: 'No suspicious verification tokens in the URL',
      modality: 'url',
    },
  ],
  research: legitimateResearch,
}

export const RESULTS_BY_ID: Record<string, AnalysisResult> = {
  [phishingResult.id]: phishingResult,
  [legitimateResult.id]: legitimateResult,
}

export function selectMockResult(url: string): AnalysisResult {
  const normalized = url.toLowerCase()
  if (normalized.includes('microsoft.com') && !normalized.includes('login-example')) {
    return {
      ...legitimateResult,
      url,
      modalities: {
        ...legitimateResult.modalities,
        url: {
          ...legitimateResult.modalities.url,
          features: { ...legitimateResult.modalities.url.features, fullUrl: url },
        },
      },
    }
  }

  return {
    ...phishingResult,
    url,
    modalities: {
      ...phishingResult.modalities,
      url: {
        ...phishingResult.modalities.url,
        features: { ...phishingResult.modalities.url.features, fullUrl: url },
      },
    },
  }
}
