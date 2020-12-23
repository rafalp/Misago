import React from "react"

interface CardMessageProps {
  children?: React.ReactNode
}

const CardMessage: React.FC<CardMessageProps> = ({ children }) => (
  <div className="card-body message-card">
    <div className="message-card-content">
      <div className="message-card-icon" />
      <div className="message-card-message">{children}</div>
    </div>
  </div>
)

export default CardMessage
