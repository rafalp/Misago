import React from "react"

interface ICardAlertProps {
  children: React.ReactNode
}

const CardAlert: React.FC<ICardAlertProps> = ({ children }) => (
  <div className="card-alert">
    <div
      className="alert alert-block alert-responsive alert-danger"
      role="alert"
    >
      {children}
    </div>
  </div>
)

export default CardAlert
