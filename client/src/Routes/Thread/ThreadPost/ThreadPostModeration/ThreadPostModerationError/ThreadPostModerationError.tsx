import { ApolloError } from "apollo-client"
import React from "react"
import { ModalCloseFooter, ModalErrorBody } from "../../../../../UI/Modal"
import { MutationError } from "../../../../../types"
import ThreadPostRootError from "../../../ThreadPostRootError"
import ThreadPostModerationErrorHeader from "./ThreadPostModerationErrorHeader"

interface ThreadPostModerationErrorProps {
  graphqlError?: ApolloError | null
  errors?: Array<MutationError> | null
  forDelete?: boolean
  close: () => void
}

const ThreadPostModerationError: React.FC<ThreadPostModerationErrorProps> = ({
  graphqlError,
  errors,
  forDelete,
  close,
}) => (
  <>
    <ThreadPostRootError graphqlError={graphqlError} dataErrors={errors}>
      {({ message }) => (
        <ModalErrorBody
          header={<ThreadPostModerationErrorHeader forDelete={forDelete} />}
          message={message}
        />
      )}
    </ThreadPostRootError>
    <ModalCloseFooter close={close} />
  </>
)

export default ThreadPostModerationError
