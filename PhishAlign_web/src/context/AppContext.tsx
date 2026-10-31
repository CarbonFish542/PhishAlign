import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'
import type { AnalysisResult } from '../types/analysis'

interface AppContextValue {
  submittedUrl: string
  setSubmittedUrl: (url: string) => void
  result: AnalysisResult | null
  setResult: (result: AnalysisResult | null) => void
  researchMode: boolean
  setResearchMode: (value: boolean) => void
}

const AppContext = createContext<AppContextValue | null>(null)

function readSession<T>(key: string, fallback: T): T {
  try {
    const raw = sessionStorage.getItem(key)
    return raw ? (JSON.parse(raw) as T) : fallback
  } catch {
    return fallback
  }
}

export function AppProvider({ children }: { children: ReactNode }) {
  const [submittedUrl, setSubmittedUrl] = useState(() => readSession('phishalign-url', ''))
  const [result, setResult] = useState<AnalysisResult | null>(() =>
    readSession<AnalysisResult | null>('phishalign-result', null),
  )
  const [researchMode, setResearchMode] = useState(() => readSession('phishalign-research', false))

  useEffect(() => {
    sessionStorage.setItem('phishalign-url', JSON.stringify(submittedUrl))
  }, [submittedUrl])

  useEffect(() => {
    if (result) sessionStorage.setItem('phishalign-result', JSON.stringify(result))
    else sessionStorage.removeItem('phishalign-result')
  }, [result])

  useEffect(() => {
    sessionStorage.setItem('phishalign-research', JSON.stringify(researchMode))
  }, [researchMode])

  const value = useMemo(
    () => ({
      submittedUrl,
      setSubmittedUrl,
      result,
      setResult,
      researchMode,
      setResearchMode,
    }),
    [submittedUrl, result, researchMode],
  )

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export function useAppState() {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error('useAppState must be used within AppProvider')
  }
  return context
}
