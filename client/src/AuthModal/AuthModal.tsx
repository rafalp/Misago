import React from "react"
import ReactDOM from "react-dom"
import { AuthModalContext } from "../Context"
import { Modal } from "../UI"
import modalsRoot from "../modalsRoot"
import { AuthModalMode, ISettings } from "../types"

import RegisterModal from "./RegisterModal"

interface IAuthModalProps {
  settings?: ISettings | null
}

const AuthModal: React.FC<IAuthModalProps> = ({ settings }) => {
  const { isOpen, mode, closeModal } = React.useContext(AuthModalContext)

  if (!settings || !modalsRoot) return null
  const root = modalsRoot

  return ReactDOM.createPortal(
    <Modal close={closeModal} isOpen={isOpen} resistant>
      {mode === AuthModalMode.REGISTER && (
        <RegisterModal settings={settings} closeModal={closeModal} />
      )}
      {mode === AuthModalMode.LOGIN && <div>LOGIN MODAL</div>}
    </Modal>,
    root
  )
}

export default AuthModal
