import { Trans } from "@lingui/macro"
import React from "react"
import { useModalContext } from "../../../../Context"
import { Modal, ModalDialog } from "../../../../UI/Modal"
import { Thread } from "../../Thread.types"
import ThreadModerationDeleteForm from "./ThreadModerationDeleteForm"

interface ThreadModerationDeleteProps {
  thread: Thread
}

const ThreadModerationDelete: React.FC<ThreadModerationDeleteProps> = ({
  thread,
}) => {
  const { isOpen, closeModal } = useModalContext()

  return (
    <Modal isOpen={isOpen} close={closeModal}>
      <ModalDialog
        title={<Trans id="moderation.delete_thread">Delete thread</Trans>}
        close={closeModal}
      >
        <ThreadModerationDeleteForm thread={thread} close={closeModal} />
      </ModalDialog>
    </Modal>
  )
}
export default ThreadModerationDelete
