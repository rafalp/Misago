import { Trans } from "@lingui/macro"
import { ApolloError } from "apollo-client"
import React from "react"
import { useModalContext } from "../../../Context"
import { Modal, ModalDialog } from "../../../UI"
import { IMutationError } from "../../../types"
import { IThread } from "../Threads.types"
import ThreadsModerationError from "./ThreadsModerationError"

interface IThreadsModerationOpenProps {
  threads: Array<IThread>
  graphqlError?: ApolloError | null
  errors?: Array<IMutationError> | null
}

const ThreadsModerationOpen: React.FC<IThreadsModerationOpenProps> = ({
  threads,
  graphqlError,
  errors,
}) => {
  const { isOpen, closeModal } = useModalContext()

  return (
    <Modal isOpen={isOpen} close={closeModal}>
      <ModalDialog
        title={<Trans id="moderation.open_threads">Open threads</Trans>}
        close={closeModal}
      >
        <ThreadsModerationError
          graphqlError={graphqlError}
          errors={errors}
          threads={threads}
          close={closeModal}
        />
      </ModalDialog>
    </Modal>
  )
}
export default ThreadsModerationOpen
