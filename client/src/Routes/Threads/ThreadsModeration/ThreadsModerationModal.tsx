import React from "react"
import { Modal, ModalDialog, portal } from "../../../UI"
import { ICategory } from "../../../types"
import { IThread } from "../Threads.types"
import {
  ThreadsModerationModalAction,
  ThreadsModerationModalContext,
} from "./ThreadsModerationModalContext"

interface IThreadsModerationModalProps {
  action: ThreadsModerationModalAction
  title: React.ReactNode
  children: (props: {
    threads: Array<IThread>
    category: ICategory | null
    close: () => void
  }) => React.ReactNode
}

const ThreadsModerationModal: React.FC<IThreadsModerationModalProps> = (
  props
) => {
  const { action, threads, category, isOpen, close } = React.useContext(
    ThreadsModerationModalContext
  )

  return portal(
    <Modal close={close} isOpen={isOpen && action === props.action}>
      <ModalDialog
        className="modal-dialog-moderation"
        close={close}
        title={props.title}
      >
        {props.children({ threads, category, close })}
      </ModalDialog>
    </Modal>
  )
}

export default ThreadsModerationModal
