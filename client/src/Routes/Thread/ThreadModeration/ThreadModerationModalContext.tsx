import { ApolloError } from "apollo-client"
import React from "react"
import { useModal } from "../../../UI"
import { IMutationError } from "../../../types"
import { IThread } from "../Thread.types"

enum ThreadModerationModalAction {
  OPEN,
  CLOSE,
  MOVE,
  DELETE,
}

interface IThreadModerationModalContext {
  isOpen: boolean
  data: IThreadModerationModalData | null
  open: (
    action: ThreadModerationModalAction,
    thread: IThread,
    data?: IThreadModerationModalDataOptional
  ) => void
  close: () => void
}

export interface IThreadModerationModalData
  extends IThreadModerationModalDataOptional {
  action: ThreadModerationModalAction
  thread: IThread
}

interface IThreadModerationModalDataOptional {
  graphqlError?: ApolloError | null
  errors?: Array<IMutationError> | null
}

const ThreadModerationModalContext = React.createContext<
  IThreadModerationModalContext
>({
  isOpen: false,
  data: null,
  open: () => {},
  close: () => {},
})

interface IThreadModerationModalContextProviderProps {
  children: React.ReactNode
}

const ThreadModerationModalContextProvider: React.FC<IThreadModerationModalContextProviderProps> = ({
  children,
}) => {
  const [action, setAction] = React.useState<ThreadModerationModalAction>(
    ThreadModerationModalAction.DELETE
  )
  const [thread, setThread] = React.useState<IThread>()
  const [graphqlError, setGraphqlError] = React.useState<ApolloError | null>(
    null
  )
  const [errors, setErrors] = React.useState<Array<IMutationError> | null>(
    null
  )
  const { isOpen, closeModal, openModal } = useModal()

  return (
    <ThreadModerationModalContext.Provider
      value={{
        isOpen,
        data: thread
          ? {
              action,
              thread,
              graphqlError,
              errors,
            }
          : null,
        open: (
          action: ThreadModerationModalAction,
          thread: IThread,
          data?: IThreadModerationModalDataOptional
        ) => {
          setAction(action)
          setThread(thread)
          if (data) {
            setGraphqlError(data?.graphqlError || null)
            setErrors(data?.errors || null)
          }
          openModal()
        },
        close: closeModal,
      }}
    >
      {children}
    </ThreadModerationModalContext.Provider>
  )
}

const useThreadModerationModalContext = (thread: IThread) => {
  const { open } = React.useContext(ThreadModerationModalContext)

  return {
    openThread: (result: {
      graphqlError?: ApolloError | null
      errors?: Array<IMutationError> | null
    }) => open(ThreadModerationModalAction.OPEN, thread, result),
    closeThread: (result: {
      graphqlError?: ApolloError | null
      errors?: Array<IMutationError> | null
    }) => open(ThreadModerationModalAction.CLOSE, thread, result),
    moveThread: () => open(ThreadModerationModalAction.MOVE, thread),
    deleteThread: () => open(ThreadModerationModalAction.DELETE, thread),
  }
}

export {
  ThreadModerationModalAction,
  ThreadModerationModalContext,
  ThreadModerationModalContextProvider,
  useThreadModerationModalContext,
}
