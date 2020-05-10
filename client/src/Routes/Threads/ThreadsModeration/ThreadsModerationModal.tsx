import React from "react"
import { Modal, ModalDialog, portal } from "../../../UI"
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
    close: () => void
  }) => React.ReactNode
}

const ThreadsModerationModal: React.FC<IThreadsModerationModalProps> = (
  props
) => {
  const { action, threads, isOpen, close } = React.useContext(
    ThreadsModerationModalContext
  )

  return portal(
    <Modal close={close} isOpen={isOpen && action === props.action}>
      <ModalDialog close={close} title={props.title}>
        {props.children({ threads, close })}
      </ModalDialog>
    </Modal>
  )
}

export default ThreadsModerationModal
