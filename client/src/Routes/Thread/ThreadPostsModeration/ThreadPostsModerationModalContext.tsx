import React from "react"
import { useModal } from "../../../UI"

interface IThreadPostsModerationModalRenderOptions {
  isOpen: boolean
  close: () => void
}

interface IThreadPostsModerationModalContext {
  isOpen: boolean
  render?: (
    options: IThreadPostsModerationModalRenderOptions
  ) => React.ReactNode
  open: (
    render: (
      options: IThreadPostsModerationModalRenderOptions
    ) => React.ReactNode
  ) => void
  close: () => void
}

const ThreadPostsModerationModalContext = React.createContext<
  IThreadPostsModerationModalContext
>({
  isOpen: false,
  open: () => {},
  close: () => {},
})

interface IThreadPostsModerationModalContextProviderProps {
  children: React.ReactNode
}

const ThreadPostsModerationModalContextProvider: React.FC<IThreadPostsModerationModalContextProviderProps> = ({
  children,
}) => {
  const [render, setRender] = React.useState<
    (options: IThreadPostsModerationModalRenderOptions) => React.ReactNode
  >()
  const { isOpen, closeModal, openModal } = useModal()

  React.useEffect(() => openModal(), [render, openModal])

  return (
    <ThreadPostsModerationModalContext.Provider
      value={{
        isOpen,
        render,
        open: (
          render: (
            options: IThreadPostsModerationModalRenderOptions
          ) => React.ReactNode
        ) => setRender(render),
        close: closeModal,
      }}
    >
      {children}
    </ThreadPostsModerationModalContext.Provider>
  )
}

const useThreadPostsModerationModalContext = () => {
  return React.useContext(ThreadPostsModerationModalContext)
}

export {
  ThreadPostsModerationModalContext,
  ThreadPostsModerationModalContextProvider,
  useThreadPostsModerationModalContext,
}
