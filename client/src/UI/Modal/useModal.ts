import React from "react"

interface ModalState {
  isOpen: boolean
  openModal: () => void
  closeModal: () => void
}

const useModal = (): ModalState => {
  const [isOpen, setState] = React.useState(false)
  const openModal = () => setState(true)
  const closeModal = () => setState(false)
  return { isOpen, openModal, closeModal }
}

export default useModal
