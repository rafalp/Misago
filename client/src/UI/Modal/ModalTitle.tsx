import React from "react"

interface IModalTitleProps {
  text: React.ReactNode
}

const ModalTitle: React.FC<IModalTitleProps> = ({ text }) => <h5 className="modal-title">{text}</h5>

export default ModalTitle