import React from "react"
import { useModal } from "../../../UI"
import { IThread } from "../Threads.types"

enum ThreadsModerationModalAction {
  DELETE,
  MOVE,
}

interface IThreadsModerationModalContext {
  isOpen: boolean
  action: ThreadsModerationModalAction
  threads: Array<IThread>
  open: (threads: Array<IThread>, action: ThreadsModerationModalAction) => void
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
  const { isOpen, closeModal, openModal } = useModal()

  return (
    <ThreadsModerationModalContext.Provider
      value={{
        isOpen,
        action,
        threads,
        open: (
          threads: Array<IThread>,
          action: ThreadsModerationModalAction
        ) => {
          setThreads(threads)
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

const useThreadModerationModalContext = (threads: Array<IThread>) => {
  const { open } = React.useContext(ThreadsModerationModalContext)

  return {
    moveThreads: () => open(threads, ThreadsModerationModalAction.MOVE),
    deleteThreads: () => open(threads, ThreadsModerationModalAction.DELETE),
  }
}

export {
  ThreadsModerationModalAction,
  ThreadsModerationModalContext,
  ThreadsModerationModalContextProvider,
  useThreadModerationModalContext,
}
