import React from "react"
import { Modal, ModalDialog, ModalFormBody } from "../"
import RootContainer from "./RootContainer"

interface ModalFormContainerProps {
  children: React.ReactNode
  title?: React.ReactNode
}

const ModalFormContainer: React.FC<ModalFormContainerProps> = ({
  children,
  title,
}) => (
  <RootContainer>
    <Modal isOpen={true} close={() => {}}>
      <ModalDialog title={title || "Modal"}>
        <ModalFormBody>{children}</ModalFormBody>
      </ModalDialog>
    </Modal>
  </RootContainer>
)

export default ModalFormContainer
