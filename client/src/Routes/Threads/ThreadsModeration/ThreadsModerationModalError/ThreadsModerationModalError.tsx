import { Trans } from "@lingui/macro"
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
import ThreadsModerationModalErrorThreads from "./ThreadsModerationModalErrorThreads"

interface IThreadsModerationModalErrorProps {
  graphqlError?: ApolloError | null
  errors?: Array<IMutationError> | null
  threads?: Array<ISelectedThread>
  close: () => void
}

const ThreadsModerationModalError: React.FC<IThreadsModerationModalErrorProps> = ({
  graphqlError,
  errors,
  threads,
  close,
}) => {
  const hasRootError = !!useRootError(errors)
  const { updated, errors: threadsErrors } = useSelectionErrors<
    ISelectedThread
  >("threads", threads, errors || [])

  if (hasRootError) {
    return (
      <RootError dataErrors={errors}>
        {({ message }) => (
          <>
            <ModalErrorBody header={<ErrorHeader />} message={message} />
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
          header={<ErrorHeader />}
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
          {threads.length === 1 ? (
            <Trans id="moderation.thread_error_header">
              Selected thread could not be updated.
            </Trans>
          ) : updated ? (
            <Trans id="moderation.threads_error_header_some">
              Some of the selected threads could not be updated.
            </Trans>
          ) : (
            <ErrorHeader />
          )}
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

const ErrorHeader: React.FC = () => (
  <Trans id="moderation.threads_error_header">
    Selected threads could not be updated.
  </Trans>
)

export default ThreadsModerationModalError
