import { Trans } from "@lingui/macro"
import { ApolloError } from "apollo-client"
import React from "react"
import {
  ModalCloseFooter,
  ModalErrorBody,
  RootError,
  ThreadValidationError,
} from "../../../../UI"
import { IMutationError } from "../../../../types"

interface IThreadModerationModalErrorProps {
  graphqlError?: ApolloError | null
  errors?: Array<IMutationError> | null
  forDelete?: boolean
  close: () => void
}

const ThreadModerationModalError: React.FC<IThreadModerationModalErrorProps> = ({
  graphqlError,
  errors,
  forDelete,
  close,
}) => (
  <RootError
    graphqlError={graphqlError}
    dataErrors={errors}
    locations={["__root__", "thread"]}
  >
    {(error) => (
      <ThreadValidationError error={error}>
        {({ message }) => (
          <>
            <ModalErrorBody
              header={
                forDelete ? (
                  <Trans id="moderation.thread_delete_error">
                    Thread could not be deleted.
                  </Trans>
                ) : (
                  <Trans id="moderation.thread_error">
                    Thread could not be updated.
                  </Trans>
                )
              }
              message={message}
            />
            <ModalCloseFooter close={close} />
          </>
        )}
      </ThreadValidationError>
    )}
  </RootError>
)

export default ThreadModerationModalError
