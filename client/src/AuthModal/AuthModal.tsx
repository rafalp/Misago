import React from "react"
import { useAuthModalContext } from "../Context"
import { Modal } from "../UI/Modal"
import portal from "../UI/portal"
import { AuthModalMode, Settings } from "../types"
import AuthModalLogin from "./AuthModalLogin"
import AuthModalRegister from "./AuthModalRegister"

interface AuthModalProps {
  settings?: Settings | null
}

const AuthModal: React.FC<AuthModalProps> = ({ settings }) => {
  const {
    isOpen,
    mode,
    closeModal,
    showLoginForm,
    showRegisterForm,
  } = useAuthModalContext()

  if (!settings) return null

  return portal(
    <Modal close={closeModal} isOpen={isOpen} resistant>
      {mode === AuthModalMode.LOGIN && (
        <AuthModalLogin close={closeModal} showRegister={showRegisterForm} />
      )}
      {mode === AuthModalMode.REGISTER && (
        <AuthModalRegister
          settings={settings}
          close={closeModal}
          showLogin={showLoginForm}
        />
      )}
    </Modal>
  )
}

export default AuthModal
