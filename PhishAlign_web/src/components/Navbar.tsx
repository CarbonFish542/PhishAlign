import { Link, NavLink } from 'react-router-dom'
import { FlaskConical, LayoutDashboard, Shield } from 'lucide-react'
import { useAppState } from '../context/AppContext'

export function Navbar() {
  const { researchMode, setResearchMode } = useAppState()

  return (
    <header className="sticky top-0 z-40 border-b border-white/6 bg-navy-950/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">
        <Link to="/" className="flex items-center gap-3">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg border border-cyan/25 bg-cyan/10">
            <Shield className="h-5 w-5 text-cyan" aria-hidden />
          </span>
          <span>
            <span className="block text-sm font-semibold tracking-tight text-ink">PhishAlign</span>
            <span className="hidden text-[11px] text-muted sm:block">
              Cross-Modal Phishing Detection
            </span>
          </span>
        </Link>

        <nav className="flex items-center gap-1 sm:gap-2" aria-label="Primary">
          <NavLink
            to="/"
            end
            className={({ isActive }) =>
              `inline-flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm ${
                isActive ? 'bg-white/6 text-ink' : 'text-muted hover:bg-white/4 hover:text-ink'
              }`
            }
          >
            <LayoutDashboard className="h-4 w-4" aria-hidden />
            <span className="hidden sm:inline">Dashboard</span>
          </NavLink>
          <NavLink
            to="/about"
            className={({ isActive }) =>
              `inline-flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm ${
                isActive ? 'bg-white/6 text-ink' : 'text-muted hover:bg-white/4 hover:text-ink'
              }`
            }
          >
            About
          </NavLink>

          <div className="ml-1 flex items-center gap-2 rounded-full border border-white/8 bg-navy-800/80 px-2.5 py-1.5">
            <FlaskConical className="h-3.5 w-3.5 text-cyan" aria-hidden />
            <span className="hidden text-xs text-muted md:inline">Research Mode</span>
            <button
              type="button"
              role="switch"
              aria-checked={researchMode}
              aria-label="Toggle research mode"
              onClick={() => setResearchMode(!researchMode)}
              className={`relative h-5 w-9 rounded-full transition-colors ${
                researchMode ? 'bg-cyan' : 'bg-navy-600'
              }`}
            >
              <span
                className={`absolute top-0.5 left-0.5 h-4 w-4 rounded-full bg-white transition-transform ${
                  researchMode ? 'translate-x-4' : 'translate-x-0'
                }`}
              />
            </button>
          </div>
        </nav>
      </div>
    </header>
  )
}
