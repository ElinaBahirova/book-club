import { createContext } from "react"

export type Theme = 'dark' | 'light' | 'system'

interface ThemeProviderState {
  theme: Theme
  setTheme: (theme: Theme) => void
  resolvedTheme: 'dark' | 'light'
}

export const ThemeProviderContext = createContext<ThemeProviderState | undefined>(undefined);
