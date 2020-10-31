import { Trans } from "@lingui/macro"
import React from "react"
import { useModalContext } from "../../../../Context"
import { Modal, ModalDialog } from "../../../../UI/Modal"
import { ICategory } from "../../../../types"
import { IThread } from "../../Threads.types"
import ThreadsModerationDeleteForm from "./ThreadsModerationDeleteForm"

interface IThreadsModerationDeleteProps {
  category?: ICategory | null
  threads: Array<IThread>
}

const ThreadsModerationDelete: React.FC<IThreadsModerationDeleteProps> = ({
  category,
  threads,
}) => {
  const { isOpen, closeModal } = useModalContext()

  return (
    <Modal isOpen={isOpen} close={closeModal}>
      <ModalDialog
        title={<Trans id="moderation.move_threads">Move threads</Trans>}
        close={closeModal}
      >
        <ThreadsModerationDeleteForm
          category={category}
          threads={threads}
          close={closeModal}
        />
      </ModalDialog>
    </Modal>
  )
}

export default ThreadsModerationDelete
