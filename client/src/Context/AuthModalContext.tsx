import React from "react"
import { useModal } from "../UI/Modal"
import { AuthModalMode } from "../types"

export interface AuthModalContextData {
  isOpen: boolean
  mode: AuthModalMode
  closeModal: () => void
  showLoginForm: () => void
  showRegisterForm: () => void
  openLoginModal: () => void
  openRegisterModal: () => void
}

const AuthModalContext = React.createContext<AuthModalContextData>({
  isOpen: false,
  mode: AuthModalMode.REGISTER,
  closeModal: () => {},
  openLoginModal: () => {},
  openRegisterModal: () => {},
  showLoginForm: () => {},
  showRegisterForm: () => {},
})

interface AuthModalProviderProps {
  children: React.ReactNode
}

const AuthModalProvider: React.FC<AuthModalProviderProps> = ({ children }) => {
  const [mode, setMode] = React.useState<AuthModalMode>(AuthModalMode.REGISTER)
  const { isOpen, closeModal, openModal } = useModal()

  const showLoginForm = () => setMode(AuthModalMode.LOGIN)
  const showRegisterForm = () => setMode(AuthModalMode.REGISTER)
  const openLoginModal = () => {
    showLoginForm()
    openModal()
  }
  const openRegisterModal = () => {
    showRegisterForm()
    openModal()
  }

  return (
    <AuthModalContext.Provider
      value={{
        isOpen,
        mode,
        closeModal,
        showLoginForm,
        showRegisterForm,
        openLoginModal,
        openRegisterModal,
      }}
    >
      {children}
    </AuthModalContext.Provider>
  )
}

const useAuthModalContext = () => React.useContext(AuthModalContext)

export { AuthModalContext, AuthModalProvider, useAuthModalContext }
