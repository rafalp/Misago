import classNames from "classnames"
import React from "react"

interface IModalFormBodyProps {
  className?: string
  children: React.ReactNode
}

const ModalFormBody: React.FC<IModalFormBodyProps> = ({
  children,
  className,
}) => (
  <div className={classNames("modal-body", "modal-form-body", className)}>
    {children}
  </div>
)

export default ModalFormBody
