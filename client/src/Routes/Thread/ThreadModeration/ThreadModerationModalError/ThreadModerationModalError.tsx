import { Trans } from "@lingui/macro"
import { ApolloError } from "apollo-client"
import React from "react"
import { ModalCloseFooter, ModalErrorBody } from "../../../../UI"
import { IMutationError } from "../../../../types"
import ThreadRootError from "../../ThreadRootError"

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
  <ThreadRootError graphqlError={graphqlError} dataErrors={errors}>
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
  </ThreadRootError>
)

export default ThreadModerationModalError
