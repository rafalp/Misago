import { Trans } from "@lingui/macro"
import React from "react"
import { Modal, ModalDialog } from "../../UI/Modal"
import portal from "../../UI/portal"
import { EditorContextData } from "../EditorContext"
import EditorControlLinkForm from "./EditorControlLinkForm"

interface EditorControlLinkModalProps {
  context: EditorContextData
  isOpen: boolean
  close: () => void
}

const EditorControlLinkModal: React.FC<EditorControlLinkModalProps> = ({
  context,
  isOpen,
  close,
}) => {
  return portal(
    <Modal isOpen={isOpen} close={close}>
      <ModalDialog
        title={<Trans id="editor.link">Insert link</Trans>}
        close={close}
      >
        <EditorControlLinkForm context={context} close={close} />
      </ModalDialog>
    </Modal>
  )
}

export default EditorControlLinkModal
