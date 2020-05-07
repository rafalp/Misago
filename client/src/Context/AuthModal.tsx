import React from "react"
import { useModal } from "../UI"
import { IAuthModalContext, AuthModalMode } from "../types"

const AuthModalContext = React.createContext<IAuthModalContext>({
  isOpen: false,
  mode: AuthModalMode.REGISTER,
  closeModal: () => {},
  openLoginModal: () => {},
  openRegisterModal: () => {},
  showLoginForm: () => {},
  showRegisterForm: () => {},
})

interface IAuthModalProviderProps {
  children: React.ReactNode
}

const AuthModalProvider: React.FC<IAuthModalProviderProps> = ({
  children,
}) => {
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

export { AuthModalContext, AuthModalProvider }
