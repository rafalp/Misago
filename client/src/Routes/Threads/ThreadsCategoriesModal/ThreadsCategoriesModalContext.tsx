import React from "react"
import { useModal } from "../../../UI"
import { IActiveCategory } from "../Threads.types"

interface IThreadsCategoriesModalContext {
  isOpen: boolean
  active?: IActiveCategory | null
  open: (active?: IActiveCategory | null) => void
  close: () => void
}

const ThreadsCategoriesModalContext = React.createContext<
  IThreadsCategoriesModalContext
>({ isOpen: false, active: null, open: () => {}, close: () => {} })

interface IThreadsCategoriesModalContextProviderProps {
  children: React.ReactNode
}

const ThreadsCategoriesModalContextProvider: React.FC<IThreadsCategoriesModalContextProviderProps> = ({
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

export { ThreadsCategoriesModalContext, ThreadsCategoriesModalContextProvider }
