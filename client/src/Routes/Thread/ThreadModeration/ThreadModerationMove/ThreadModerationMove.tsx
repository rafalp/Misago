import { Trans } from "@lingui/macro"
import React from "react"
import { useModalContext } from "../../../../Context"
import { Modal, ModalDialog } from "../../../../UI/Modal"
import { Thread } from "../../Thread.types"
import ThreadModerationMoveForm from "./ThreadModerationMoveForm"

interface ThreadModerationMoveProps {
  thread: Thread
}

const ThreadModerationMove: React.FC<ThreadModerationMoveProps> = ({
  thread,
}) => {
  const { isOpen, closeModal } = useModalContext()

  return (
    <Modal isOpen={isOpen} close={closeModal}>
      <ModalDialog
        title={<Trans id="moderation.delete_thread">Move thread</Trans>}
        close={closeModal}
      >
        <ThreadModerationMoveForm thread={thread} close={closeModal} />
      </ModalDialog>
    </Modal>
  )
}
export default ThreadModerationMove
