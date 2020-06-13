import React from "react"
import { Modal, ModalDialog, portal } from "../../../UI"
import {
  IThreadModerationModalData,
  ThreadModerationModalAction,
  ThreadModerationModalContext,
} from "./ThreadModerationModalContext"

interface IThreadModerationModalProps {
  action: ThreadModerationModalAction
  title: React.ReactNode
  children: (props: {
    data: IThreadModerationModalData
    close: () => void
  }) => React.ReactNode
}

const ThreadModerationModal: React.FC<IThreadModerationModalProps> = (
  props
) => {
  const { data, isOpen, close } = React.useContext(
    ThreadModerationModalContext
  )

  return portal(
    <Modal
      close={close}
      isOpen={isOpen && data ? data.action === props.action : false}
      resistant
    >
      <ModalDialog
        className="modal-dialog-moderation"
        close={close}
        title={props.title}
      >
        {data && props.children({ data, close })}
      </ModalDialog>
    </Modal>
  )
}

export default ThreadModerationModal
