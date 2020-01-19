import React from "react"
import ReactDOM from "react-dom"
import { AuthModalContext } from "../Context"
import { Modal } from "../UI"
import modalsRoot from "../modalsRoot"
import { AuthModalMode, ISettings } from "../types"
import LoginModal from "./LoginModal"
import RegisterModal from "./RegisterModal"

interface IAuthModalProps {
  settings?: ISettings | null
}

const AuthModal: React.FC<IAuthModalProps> = ({ settings }) => {
  const {
    isOpen,
    mode,
    closeModal,
    showLoginForm,
    showRegisterForm,
  } = React.useContext(AuthModalContext)

  if (!settings || !modalsRoot) return null
  const root = modalsRoot

  return ReactDOM.createPortal(
    <Modal close={closeModal} isOpen={isOpen} resistant>
      {mode === AuthModalMode.LOGIN && (
        <LoginModal close={closeModal} showRegister={showRegisterForm} />
      )}
      {mode === AuthModalMode.REGISTER && (
        <RegisterModal
          settings={settings}
          close={closeModal}
          showLogin={showLoginForm}
        />
      )}
    </Modal>,
    root
  )
}

export default AuthModal
