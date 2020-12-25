import React from "react"
import { useModal } from "../../../UI/Modal"
import { ActiveCategory } from "../Threads.types"

interface ThreadsCategoriesModalContextData {
  isOpen: boolean
  active?: ActiveCategory | null
  open: (active?: ActiveCategory | null) => void
  close: () => void
}

const ThreadsCategoriesModalContext = React.createContext<ThreadsCategoriesModalContextData>(
  { isOpen: false, active: null, open: () => {}, close: () => {} }
)

interface ThreadsCategoriesModalContextProviderProps {
  children: React.ReactNode
}

const ThreadsCategoriesModalContextProvider: React.FC<ThreadsCategoriesModalContextProviderProps> = ({
  children,
}) => {
  const [active, setActive] = React.useState<ActiveCategory | null>(null)
  const { isOpen, closeModal, openModal } = useModal()

  return (
    <ThreadsCategoriesModalContext.Provider
      value={{
        isOpen,
        active,
        open: (active?: ActiveCategory | null) => {
          setActive(active || null)
          openModal()
        },
        close: closeModal,
      }}
    >
      {children}
    </ThreadsCategoriesModalContext.Provider>
  )
}

const useThreadsCategoriesModalContext = () => {
  return React.useContext(ThreadsCategoriesModalContext)
}

export {
  ThreadsCategoriesModalContext,
  ThreadsCategoriesModalContextProvider,
  useThreadsCategoriesModalContext,
}
