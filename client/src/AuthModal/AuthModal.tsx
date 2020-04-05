import React from "react"
import { AuthModalContext } from "../Context"
import { Modal, portal } from "../UI"
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

  if (!settings) return null

  return portal(
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
    </Modal>
  )
}

export default AuthModal
