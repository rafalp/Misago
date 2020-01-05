import { Trans } from "@lingui/macro"
import React from "react"
import ReactDOM from "react-dom"
import { Modal, ModalBody } from "../UI"
import root from "../modalsRoot"
import { ISettings } from "../types"

interface IRegisterModalProps {
  isOpen: boolean
  settings: ISettings | null
  closeModal: () => void
}

const RegisterModal: React.FC<IRegisterModalProps> = ({ isOpen, settings, closeModal }) => {
  if (!settings || !root) return null

  return ReactDOM.createPortal(
    <Modal
      className="modal-register"
      close={closeModal}
      isOpen={isOpen}
      title={<Trans>Register</Trans>}
    >
      <ModalBody>REGISTER MODAL</ModalBody>
    </Modal>,
    root
  )
}

export default RegisterModal
