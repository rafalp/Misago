import React from "react"

interface IToast {
  id: string
  text: React.ReactNode
}

interface IToastsContext {
  toasts: Array<IToast>
  showToast: (text: React.ReactNode) => string
  removeToast: (id: string) => void
}

const ToastsContext = React.createContext<IToastsContext>({
  toasts: [],
  showToast: () => "null",
  removeToast: () => {},
})

interface IToastsProviderProps {
  children: React.ReactNode
}

const TOASTS_LIMIT = 5

const ToastsProvider: React.FC<IToastsProviderProps> = ({ children }) => {
  const [state, setState] = React.useState<Array<IToast>>([])

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
