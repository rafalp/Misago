import classnames from "classnames"
import React from "react"

interface IModalErrorBodyProps {
  className?: string | null
  header: React.ReactNode | null
  message?: React.ReactNode | null
}

const ModalErrorBody: React.FC<IModalErrorBodyProps> = ({
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
