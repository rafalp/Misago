import classnames from "classnames"
import React from "react"

interface ModalFormBodyProps {
  className?: string
  children: React.ReactNode
}

const ModalFormBody: React.FC<ModalFormBodyProps> = ({
  children,
  className,
}) => (
  <div className={classnames("modal-body", "modal-form-body", className)}>
    {children}
  </div>
)

export default ModalFormBody
