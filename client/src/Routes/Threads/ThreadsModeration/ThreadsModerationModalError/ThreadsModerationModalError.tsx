import { ApolloError } from "apollo-client"
import React from "react"
import {
  ErrorMessage,
  GraphQLErrorMessage,
  GraphQLErrorRenderer,
  ModalAlert,
  ModalCloseFooter,
  ModalErrorBody,
  RootError,
  useRootError,
  useSelectionErrors,
} from "../../../../UI"
import { IMutationError } from "../../../../types"
import { ISelectedThread } from "../../Threads.types"
import ThreadsModerationModalErrorHeader from "./ThreadsModerationModalErrorHeader"
import ThreadsModerationModalErrorThreads from "./ThreadsModerationModalErrorThreads"

interface IThreadsModerationModalErrorProps {
  graphqlError?: ApolloError | null
  errors?: Array<IMutationError> | null
  forDelete?: boolean
  threads?: Array<ISelectedThread>
  close: () => void
}

const ThreadsModerationModalError: React.FC<IThreadsModerationModalErrorProps> = ({
  graphqlError,
  errors,
  forDelete,
  threads,
  close,
}) => {
  const hasRootError = !!useRootError(errors)
  const { errors: threadsErrors } = useSelectionErrors<ISelectedThread>(
    "threads",
    threads,
    errors || []
  )

  if (hasRootError) {
    return (
      <RootError dataErrors={errors}>
        {({ message }) => (
          <>
            <ModalErrorBody
              header={
                <ThreadsModerationModalErrorHeader forDelete={forDelete} />
              }
              message={message}
            />
            <ModalCloseFooter close={close} />
          </>
        )}
      </RootError>
    )
  }

  if (graphqlError) {
    return (
      <>
        <ModalErrorBody
          header={<ThreadsModerationModalErrorHeader forDelete={forDelete} />}
          message={
            <GraphQLErrorRenderer
              error={graphqlError}
              networkError={<GraphQLErrorMessage />}
              queryError={<ErrorMessage />}
            />
          }
        />
        <ModalCloseFooter close={close} />
      </>
    )
  }

  if (threads) {
    return (
      <>
        <ModalAlert>
          <ThreadsModerationModalErrorHeader
            forDelete={forDelete}
            threads={threads}
            threadsErrors={threadsErrors}
          />
        </ModalAlert>
        <ThreadsModerationModalErrorThreads
          errors={threadsErrors}
          threads={threads}
        />
        <ModalCloseFooter close={close} />
      </>
    )
  }

  return null
}

export default ThreadsModerationModalError
