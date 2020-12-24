import React from "react"

interface CardAlertProps {
  children: React.ReactNode
}

const CardAlert: React.FC<CardAlertProps> = ({ children }) => (
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
