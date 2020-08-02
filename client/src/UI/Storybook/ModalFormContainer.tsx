import React from "react"
import {
  ButtonPrimary,
  Modal,
  ModalDialog,
  ModalFormBody,
  ModalFooter,
} from "../"
import RootContainer from "./RootContainer"

interface ModalFormContainerProps {
  children: React.ReactNode
  title?: React.ReactNode
  footer?: boolean
}

const ModalFormContainer: React.FC<ModalFormContainerProps> = ({
  children,
  title,
  footer,
}) => (
  <RootContainer>
    <Modal isOpen={true} close={() => {}}>
      <ModalDialog title={title || "Modal"}>
        <ModalFormBody>{children}</ModalFormBody>
        {footer && (
          <ModalFooter>
            <ButtonPrimary text="Submit" onClick={() => {}} responsive />
          </ModalFooter>
        )}
      </ModalDialog>
    </Modal>
  </RootContainer>
)

export default ModalFormContainer
