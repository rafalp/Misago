import classnames from "classnames"
import React from "react"

interface ModalErrorBodyProps {
  className?: string | null
  header: React.ReactNode
  message?: React.ReactNode
}

const ModalErrorBody: React.FC<ModalErrorBodyProps> = ({
  className,
  header,
  message,
}) => (
  <div className={classnames("modal-body", "modal-error", className)}>
    <div className="modal-error-body">
      <div className="modal-error-icon" />
      <div className="modal-error-message">
        <p className="lead">{header}</p>
        {message && <p>{message}</p>}
      </div>
    </div>
  </div>
)

export default ModalErrorBody
