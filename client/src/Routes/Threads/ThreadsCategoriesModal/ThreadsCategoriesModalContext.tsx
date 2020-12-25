import React from "react"
import { useModal } from "../../../UI/Modal"
import { IActiveCategory } from "../Threads.types"

interface ThreadsCategoriesModalContext {
  isOpen: boolean
  active?: IActiveCategory | null
  open: (active?: IActiveCategory | null) => void
  close: () => void
}

const ThreadsCategoriesModalContext = React.createContext<ThreadsCategoriesModalContext>(
  { isOpen: false, active: null, open: () => {}, close: () => {} }
)

interface ThreadsCategoriesModalContextProviderProps {
  children: React.ReactNode
}

const ThreadsCategoriesModalContextProvider: React.FC<ThreadsCategoriesModalContextProviderProps> = ({
  children,
}) => {
  const [active, setActive] = React.useState<IActiveCategory | null>(null)
  const { isOpen, closeModal, openModal } = useModal()

  return (
    <ThreadsCategoriesModalContext.Provider
      value={{
        isOpen,
        active,
        open: (active?: IActiveCategory | null) => {
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
