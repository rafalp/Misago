import { Trans } from "@lingui/macro"
import React from "react"
import { Modal, ModalDialog } from "../../UI/Modal"
import portal from "../../UI/portal"
import { IEditorContextValues } from "../EditorContext"
import EditorControlCodeForm from "./EditorControlCodeForm"

interface IEditorControlCodeModalProps {
  context: IEditorContextValues
  isOpen: boolean
  close: () => void
}

const EditorControlCodeModal: React.FC<IEditorControlCodeModalProps> = ({
  context,
  isOpen,
  close,
}) => {
  return portal(
    <Modal isOpen={isOpen} close={close}>
      <ModalDialog
        title={<Trans id="editor.code">Insert code</Trans>}
        close={close}
      >
        <EditorControlCodeForm context={context} close={close} />
      </ModalDialog>
    </Modal>
  )
}

export default EditorControlCodeModal
