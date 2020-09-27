import classnames from "classnames"
import React from "react"

interface IModalMessageBodyProps {
  actions?: React.ReactNode | null
  className?: string | null
  header: React.ReactNode | null
  message?: React.ReactNode | null
}

const ModalMessageBody: React.FC<IModalMessageBodyProps> = ({
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
