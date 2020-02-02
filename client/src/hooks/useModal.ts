import React from "react"

interface IModalState {
  isOpen: boolean
  openModal: () => void
  closeModal: () => void
}

const useModal = (): IModalState => {
  const [isOpen, setState] = React.useState(false)
  const openModal = () => setState(true)
  const closeModal = () => setState(false)
  return { isOpen, openModal, closeModal }
}

export default useModal
