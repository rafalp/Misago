import React from "react"
import { Modal, ModalDialog } from "../Modal"
import RootContainer from "./RootContainer"

interface ModalContainerProps {
  children: React.ReactNode
  title?: React.ReactNode
  close?: () => void
}

const ModalContainer: React.FC<ModalContainerProps> = ({
  children,
  title,
  close,
}) => (
  <RootContainer>
    <Modal isOpen={true} close={close || (() => {})}>
      <ModalDialog title={title || "Modal"}>{children}</ModalDialog>
    </Modal>
  </RootContainer>
)

export default ModalContainer
