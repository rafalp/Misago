import React from "react"

interface ModalTitleProps {
  text: React.ReactNode
}

const ModalTitle: React.FC<ModalTitleProps> = ({ text }) => (
  <h5 className="modal-title">{text}</h5>
)

export default ModalTitle
