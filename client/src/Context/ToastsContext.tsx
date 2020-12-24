import React from "react"

interface Toast {
  id: string
  text: React.ReactNode
}

interface ToastsContextData {
  toasts: Array<Toast>
  showToast: (text: React.ReactNode) => string
  removeToast: (id: string) => void
}

const ToastsContext = React.createContext<ToastsContextData>({
  toasts: [],
  showToast: () => "null",
  removeToast: () => {},
})

interface ToastsProviderProps {
  children: React.ReactNode
}

const TOASTS_LIMIT = 5

const ToastsProvider: React.FC<ToastsProviderProps> = ({ children }) => {
  const [state, setState] = React.useState<Array<Toast>>([])

  return (
    <ToastsContext.Provider
      value={{
        toasts: state,
        showToast: (text: React.ReactNode) => {
          const id = new Date().toISOString()
          setState((prevState) => {
            const state = [...prevState, { id, text }]
            if (state.length > TOASTS_LIMIT) {
              return state.slice(state.length - TOASTS_LIMIT)
            }
            return state
          })
          return id
        },
        removeToast: (id: string) => {
          setState((state) => {
            return state.filter((toast) => toast.id !== id)
          })
        },
      }}
    >
      {children}
    </ToastsContext.Provider>
  )
}

const useToastsContext = () => React.useContext(ToastsContext)

export { ToastsContext, ToastsProvider, useToastsContext }
