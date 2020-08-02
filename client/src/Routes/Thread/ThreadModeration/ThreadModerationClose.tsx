import { Trans } from "@lingui/macro"
import { ApolloError } from "apollo-client"
import React from "react"
import { useModalContext } from "../../../Context"
import { Modal, ModalDialog } from "../../../UI"
import { IMutationError } from "../../../types"
import ThreadModerationError from "./ThreadModerationError"

interface IThreadModerationCloseProps {
  graphqlError?: ApolloError | null
  errors?: Array<IMutationError> | null
}

const ThreadModerationClose: React.FC<IThreadModerationCloseProps> = ({
  graphqlError,
  errors,
}) => {
  const { isOpen, closeModal } = useModalContext()

  return (
    <Modal isOpen={isOpen} close={closeModal}>
      <ModalDialog
        title={<Trans id="moderation.close_thread">Close thread</Trans>}
        close={closeModal}
      >
        <ThreadModerationError
          graphqlError={graphqlError}
          errors={errors}
          close={closeModal}
        />
      </ModalDialog>
    </Modal>
  )
}

export default ThreadModerationClose
