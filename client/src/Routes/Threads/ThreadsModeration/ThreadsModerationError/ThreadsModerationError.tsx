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
import ThreadsModerationErrorHeader from "./ThreadsModerationErrorHeader"
import ThreadsModerationErrorThreads from "./ThreadsModerationErrorThreads"

interface IThreadsModerationErrorProps {
  graphqlError?: ApolloError | null
  errors?: Array<IMutationError> | null
  forDelete?: boolean
  threads?: Array<ISelectedThread>
  close: () => void
}

const ThreadsModerationError: React.FC<IThreadsModerationErrorProps> = ({
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
              header={<ThreadsModerationErrorHeader forDelete={forDelete} />}
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
          header={<ThreadsModerationErrorHeader forDelete={forDelete} />}
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
          <ThreadsModerationErrorHeader
            forDelete={forDelete}
            threads={threads}
            threadsErrors={threadsErrors}
          />
        </ModalAlert>
        <ThreadsModerationErrorThreads
          errors={threadsErrors}
          threads={threads}
        />
        <ModalCloseFooter close={close} />
      </>
    )
  }

  return null
}

export default ThreadsModerationError
