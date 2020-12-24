import React from "react"
import { useModal } from "../UI/Modal"
import portal from "../UI/portal"

interface ModalContext {
  isOpen: boolean
  component: React.ReactNode
  openModal: (component: React.ReactNode) => void
  closeModal: () => void
}

const ModalContext = React.createContext<ModalContext>({
  isOpen: false,
  component: null,
  openModal: () => {},
  closeModal: () => {},
})

interface ModalProviderProps {
  children: React.ReactNode
}

const ModalProvider: React.FC<ModalProviderProps> = ({ children }) => {
  const [component, setComponent] = React.useState<React.ReactNode>()
  const { isOpen, closeModal, openModal } = useModal()

  return (
    <ModalContext.Provider
      value={{
        isOpen,
        component,
        closeModal,
        openModal: (component: React.ReactNode) => {
          setComponent(component)
          window.setTimeout(openModal, 0)
        },
      }}
    >
      {children}
    </ModalContext.Provider>
  )
}

const ModalConsumer: React.FC = () => (
  <ModalContext.Consumer>
    {({ component }) => (component ? portal(component) : null)}
  </ModalContext.Consumer>
)

const useModalContext = () => React.useContext(ModalContext)

export { ModalContext, ModalConsumer, ModalProvider, useModalContext }
