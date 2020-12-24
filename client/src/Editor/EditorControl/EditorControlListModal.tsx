import { Trans } from "@lingui/macro"
import React from "react"
import { Modal, ModalDialog } from "../../UI/Modal"
import portal from "../../UI/portal"
import { EditorContextData } from "../EditorContext"
import EditorControlListForm from "./EditorControlListForm"

interface EditorControlListModalProps {
  context: EditorContextData
  isOpen: boolean
  close: () => void
}

const EditorControlListModal: React.FC<EditorControlListModalProps> = ({
  context,
  isOpen,
  close,
}) => {
  return portal(
    <Modal isOpen={isOpen} close={close}>
      <ModalDialog
        title={<Trans id="editor.list">Insert list</Trans>}
        close={close}
      >
        <EditorControlListForm context={context} close={close} />
      </ModalDialog>
    </Modal>
  )
}

export default EditorControlListModal
