import classNames from "classnames"
import React from "react"

interface IModalMessageBodyProps {
  className?: string | null
  header: React.ReactNode | null
  message?: React.ReactNode | null
}

const ModalMessageBody: React.FC<IModalMessageBodyProps> = ({
  className,
  header,
  message,
}) => (
  <div className={classNames("modal-body", "modal-message", className)}>
    <div className="modal-message-body">
      <div className="modal-message-icon" />
      <div className="modal-message-message">
        <p className="lead">{header}</p>
        {message && <p>{message}</p>}
      </div>
    </div>
  </div>
)

export default ModalMessageBody
