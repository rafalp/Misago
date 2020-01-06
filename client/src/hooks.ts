import React from "react"

interface IModalState {
  isOpen: boolean
  openModal: () => void
  closeModal: () => void
}

export const useModalState = (): IModalState => {
  const [isOpen, updateOpen] = React.useState(false)
  const openModal = () => updateOpen(true)
  const closeModal = () => updateOpen(false)
  return { isOpen, openModal, closeModal }
}
