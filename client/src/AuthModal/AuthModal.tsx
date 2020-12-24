import React from "react"
import { useAuthModalContext } from "../Context"
import { Modal } from "../UI/Modal"
import portal from "../UI/portal"
import { AuthModalMode, Settings } from "../types"
import LoginModal from "./LoginModal"
import RegisterModal from "./RegisterModal"

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
