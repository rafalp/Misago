import { Trans } from "@lingui/macro"
import { ApolloError } from "apollo-client"
import React from "react"
import { useModalContext } from "../../../Context"
import { Modal, ModalDialog } from "../../../UI/Modal"
import { IMutationError } from "../../../types"
import ThreadModerationError from "./ThreadModerationError"

interface IThreadModerationOpenProps {
  graphqlError?: ApolloError | null
  errors?: Array<IMutationError> | null
}

const ThreadModerationOpen: React.FC<IThreadModerationOpenProps> = ({
  graphqlError,
  errors,
}) => {
  const { isOpen, closeModal } = useModalContext()

  return (
    <Modal isOpen={isOpen} close={closeModal}>
      <ModalDialog
        title={<Trans id="moderation.open_thread">Open thread</Trans>}
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

export default ThreadModerationOpen
