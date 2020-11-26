import React from "react"

interface IModalAlertProps {
  children: React.ReactNode
}

const ModalAlert: React.FC<IModalAlertProps> = ({ children }) => (
  <div className="modal-alert">
    <div
      className="alert alert-block alert-responsive alert-danger"
      role="alert"
    >
      {children}
    </div>
  </div>
)

export default ModalAlert
