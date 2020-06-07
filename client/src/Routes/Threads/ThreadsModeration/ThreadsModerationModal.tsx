import React from "react"
import { Modal, ModalDialog, portal } from "../../../UI"
import {
  IThreadsModerationModalData,
  ThreadsModerationModalAction,
  ThreadsModerationModalContext,
} from "./ThreadsModerationModalContext"

interface IThreadsModerationModalProps {
  action: ThreadsModerationModalAction
  title: React.ReactNode
  children: (props: {
    data: IThreadsModerationModalData
    close: () => void
  }) => React.ReactNode
}

const ThreadsModerationModal: React.FC<IThreadsModerationModalProps> = (
  props
) => {
  const { data, isOpen, close } = React.useContext(
    ThreadsModerationModalContext
  )

  return portal(
    <Modal close={close} isOpen={isOpen && data.action === props.action}>
      <ModalDialog
        className="modal-dialog-moderation"
        close={close}
        title={props.title}
      >
        {props.children({ data, close })}
      </ModalDialog>
    </Modal>
  )
}

export default ThreadsModerationModal
