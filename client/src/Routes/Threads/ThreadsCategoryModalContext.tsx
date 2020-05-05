import React from "react"
import { useModal } from "../../hooks"
import { IActiveCategory } from "./Threads.types"

interface IThreadsCategoryModalContext {
  isOpen: boolean
  active?: IActiveCategory | null
  open: (active?: IActiveCategory | null) => void
  close: () => void
}

const ThreadsCategoryModalContext = React.createContext<
  IThreadsCategoryModalContext
>({ isOpen: false, active: null, open: () => {}, close: () => {} })

interface IThreadsCategoryModalContextProviderProps {
  children: React.ReactNode
}

const ThreadsCategoryModalContextProvider: React.FC<IThreadsCategoryModalContextProviderProps> = ({
  children,
}) => {
  const [active, setActive] = React.useState<IActiveCategory | null>(null)
  const { isOpen, closeModal, openModal } = useModal()

  return (
    <ThreadsCategoryModalContext.Provider
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
    </ThreadsCategoryModalContext.Provider>
  )
}

export { ThreadsCategoryModalContext, ThreadsCategoryModalContextProvider }
