import classnames from "classnames"
import React from "react"

interface ModalMessageBodyProps {
  actions?: React.ReactNode
  className?: string | null
  header: React.ReactNode
  message?: React.ReactNode
}

const ModalMessageBody: React.FC<ModalMessageBodyProps> = ({
  actions,
  className,
  header,
  message,
}) => (
  <div className={classnames("modal-body", "modal-message", className)}>
    <div className="modal-message-body">
      <div className="modal-message-icon" />
      <div className="modal-message-message">
        <p className="lead">{header}</p>
        {message && <p>{message}</p>}
        {actions && <div className="modal-message-actions">{actions}</div>}
      </div>
    </div>
  </div>
)

export default ModalMessageBody
