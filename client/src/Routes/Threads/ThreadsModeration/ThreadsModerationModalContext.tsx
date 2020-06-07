import { ApolloError } from "apollo-client"
import React from "react"
import { useModal } from "../../../UI"
import { ICategory, IMutationError } from "../../../types"
import { IThread } from "../Threads.types"

enum ThreadsModerationModalAction {
  OPEN,
  CLOSE,
  MOVE,
  DELETE,
}

interface IThreadsModerationModalContext {
  isOpen: boolean
  data: IThreadsModerationModalData
  open: (
    action: ThreadsModerationModalAction,
    threads: Array<IThread>,
    data?: IThreadsModerationModalDataOptional
  ) => void
  close: () => void
}

export interface IThreadsModerationModalData
  extends IThreadsModerationModalDataOptional {
  action: ThreadsModerationModalAction
  threads: Array<IThread>
}

interface IThreadsModerationModalDataOptional {
  category?: ICategory | null
  graphqlError?: ApolloError | null
  errors?: Array<IMutationError> | null
}

const ThreadsModerationModalContext = React.createContext<
  IThreadsModerationModalContext
>({
  isOpen: false,
  data: {
    action: ThreadsModerationModalAction.DELETE,
    threads: [],
    category: null,
    graphqlError: null,
    errors: null,
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
  const [graphqlError, setGraphqlError] = React.useState<ApolloError | null>(
    null
  )
  const [errors, setErrors] = React.useState<Array<IMutationError> | null>(
    null
  )
  const { isOpen, closeModal, openModal } = useModal()

  return (
    <ThreadsModerationModalContext.Provider
      value={{
        isOpen,
        data: {
          action,
          threads,
          category,
          graphqlError,
          errors,
        },
        open: (
          action: ThreadsModerationModalAction,
          threads: Array<IThread>,
          data?: IThreadsModerationModalDataOptional
        ) => {
          setAction(action)
          setThreads(threads)
          if (data) {
            setCategory(data?.category || null)
            setGraphqlError(data?.graphqlError || null)
            setErrors(data?.errors || null)
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
    openThreads: (result: {
      graphqlError?: ApolloError | null
      errors?: Array<IMutationError> | null
    }) => open(ThreadsModerationModalAction.OPEN, threads, result),
    closeThreads: (result: {
      graphqlError?: ApolloError | null
      errors?: Array<IMutationError> | null
    }) => open(ThreadsModerationModalAction.CLOSE, threads, result),
    moveThreads: () => open(ThreadsModerationModalAction.MOVE, threads),
    deleteThreads: () =>
      open(ThreadsModerationModalAction.DELETE, threads, {
        category,
      }),
  }
}

export {
  ThreadsModerationModalAction,
  ThreadsModerationModalContext,
  ThreadsModerationModalContextProvider,
  useThreadsModerationModalContext,
}
