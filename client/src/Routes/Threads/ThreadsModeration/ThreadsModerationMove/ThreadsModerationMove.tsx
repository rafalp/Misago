import { Trans } from "@lingui/macro"
import React from "react"
import { useModalContext } from "../../../../Context"
import { Modal, ModalDialog } from "../../../../UI"
import { IThread } from "../../Threads.types"
import ThreadsModerationMoveForm from "./ThreadsModerationMoveForm"

interface IThreadsModerationMoveProps {
  threads: Array<IThread>
}

const ThreadsModerationMove: React.FC<IThreadsModerationMoveProps> = ({
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
