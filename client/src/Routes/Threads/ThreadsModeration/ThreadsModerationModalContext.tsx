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
  data: {
    action: ThreadsModerationModalAction
    threads: Array<IThread>
    category: ICategory | null
  }
  open: (
    action: ThreadsModerationModalAction,
    threads: Array<IThread>,
    data?: {
      category?: ICategory | null
    }
  ) => void
  close: () => void
}

const ThreadsModerationModalContext = React.createContext<
  IThreadsModerationModalContext
>({
  isOpen: false,
  data: {
    action: ThreadsModerationModalAction.DELETE,
    threads: [],
    category: null,
  },
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
  const [category, setCategory] = React.useState<ICategory | null>(null)
  const { isOpen, closeModal, openModal } = useModal()

  return (
    <ThreadsModerationModalContext.Provider
      value={{
        isOpen,
        data: {
          action,
          threads,
          category,
        },
        open: (
          action: ThreadsModerationModalAction,
          threads: Array<IThread>,
          data?: {
            category?: ICategory | null
          }
        ) => {
          setAction(action)
          setThreads(threads)
          if (data) {
            setCategory(data?.category || null)
          }
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
    moveThreads: () => open(ThreadsModerationModalAction.MOVE, threads),
    deleteThreads: () =>
      open(ThreadsModerationModalAction.DELETE, threads, {
        category: category,
      }),
  }
}

export {
  ThreadsModerationModalAction,
  ThreadsModerationModalContext,
  ThreadsModerationModalContextProvider,
  useThreadsModerationModalContext,
}
