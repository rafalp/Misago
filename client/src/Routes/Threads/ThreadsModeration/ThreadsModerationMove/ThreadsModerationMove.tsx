import { Trans } from "@lingui/macro"
import React from "react"
import { useModalContext } from "../../../../Context"
import { Modal, ModalDialog } from "../../../../UI/Modal"
import { Thread } from "../../Threads.types"
import ThreadsModerationMoveForm from "./ThreadsModerationMoveForm"

interface ThreadsModerationMoveProps {
  threads: Array<Thread>
}

const ThreadsModerationMove: React.FC<ThreadsModerationMoveProps> = ({
  threads,
}) => {
  const { isOpen, closeModal } = useModalContext()

  return (
    <Modal isOpen={isOpen} close={closeModal}>
      <ModalDialog
        title={<Trans id="moderation.move_threads">Move threads</Trans>}
        close={closeModal}
      >
        <ThreadsModerationMoveForm threads={threads} close={closeModal} />
      </ModalDialog>
    </Modal>
  )
}

export default ThreadsModerationMove
