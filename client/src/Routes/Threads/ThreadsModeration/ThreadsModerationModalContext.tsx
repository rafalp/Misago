import React from "react"
import { useModal } from "../../../UI"
import { ICategory } from "../../../types"
import { IThread } from "../Threads.types"

enum ThreadsModerationModalAction {
  DELETE,
  MOVE,
}

interface IThreadsModerationModalContext {
  isOpen: boolean
  action: ThreadsModerationModalAction
  threads: Array<IThread>
  category?: ICategory | null
  open: (
    threads: Array<IThread>,
    category: ICategory | null | undefined,
    action: ThreadsModerationModalAction
  ) => void
  close: () => void
}

const ThreadsModerationModalContext = React.createContext<
  IThreadsModerationModalContext
>({
  isOpen: false,
  action: ThreadsModerationModalAction.DELETE,
  threads: [],
  open: () => {},
  close: () => {},
})

interface IThreadsModerationModalContextProviderProps {
  children: React.ReactNode
}

const ThreadsModerationModalContextProvider: React.FC<IThreadsModerationModalContextProviderProps> = ({
  children,
}) => {
  const [action, setAction] = React.useState<ThreadsModerationModalAction>(
    ThreadsModerationModalAction.DELETE
  )
  const [threads, setThreads] = React.useState<Array<IThread>>([])
  const [category, setCategory] = React.useState<ICategory | null>()
  const { isOpen, closeModal, openModal } = useModal()

  return (
    <ThreadsModerationModalContext.Provider
      value={{
        isOpen,
        action,
        threads,
        category,
        open: (
          threads: Array<IThread>,
          category: ICategory | null | undefined,
          action: ThreadsModerationModalAction
        ) => {
          setThreads(threads)
          setCategory(category)
          setAction(action)
          openModal()
        },
        close: closeModal,
      }}
    >
      {children}
    </ThreadsModerationModalContext.Provider>
  )
}

const useThreadsModerationModalContext = (
  threads: Array<IThread>,
  category?: ICategory | null
) => {
  const { open } = React.useContext(ThreadsModerationModalContext)

  return {
    moveThreads: () =>
      open(threads, category, ThreadsModerationModalAction.MOVE),
    deleteThreads: () =>
      open(threads, category, ThreadsModerationModalAction.DELETE),
  }
}

export {
  ThreadsModerationModalAction,
  ThreadsModerationModalContext,
  ThreadsModerationModalContextProvider,
  useThreadsModerationModalContext,
}
