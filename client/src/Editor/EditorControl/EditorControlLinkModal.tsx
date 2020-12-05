import { Trans } from "@lingui/macro"
import React from "react"
import { Modal, ModalDialog } from "../../UI/Modal"
import portal from "../../UI/portal"
import { IEditorContextValues } from "../EditorContext"
import EditorControlLinkForm from "./EditorControlLinkForm"

interface IEditorControlLinkModalProps {
  context: IEditorContextValues
  isOpen: boolean
  close: () => void
}

const EditorControlLinkModal: React.FC<IEditorControlLinkModalProps> = ({
  context,
  isOpen,
  close,
}) => {
  return portal(
    <Modal isOpen={isOpen} close={close}>
      <ModalDialog
        title={<Trans id="editor.link_modal.title">Insert link</Trans>}
        close={close}
      >
        <EditorControlLinkForm context={context} close={close} />
      </ModalDialog>
    </Modal>
  )
}

export default EditorControlLinkModal
