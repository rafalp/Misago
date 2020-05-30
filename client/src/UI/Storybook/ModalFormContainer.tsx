import React from "react"
import { Form, Modal, ModalDialog, ModalFormBody } from "../"
import RootContainer from "./RootContainer"

interface ModalFormContainerProps {
  children: React.ReactNode
  title?: React.ReactNode
}

const ModalFormContainer: React.FC<ModalFormContainerProps> = ({
  children,
  title,
}) => (
  <Form>
    <RootContainer>
      <Modal isOpen={true} close={() => {}}>
        <ModalDialog title={title || "Modal"}>
          <ModalFormBody>{children}</ModalFormBody>
        </ModalDialog>
      </Modal>
    </RootContainer>
  </Form>
)

export default ModalFormContainer
