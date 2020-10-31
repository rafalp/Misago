import { Trans } from "@lingui/macro"
import React from "react"
import { useModalContext } from "../../../../Context"
import { Modal, ModalDialog } from "../../../../UI/Modal"
import { IThread } from "../../Thread.types"
import ThreadModerationDeleteForm from "./ThreadModerationDeleteForm"

interface IThreadModerationDeleteProps {
  thread: IThread
}

const ThreadModerationDelete: React.FC<IThreadModerationDeleteProps> = ({
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
