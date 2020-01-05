import classNames from "classnames"
import React from "react"

interface IModalBodyProps {
  className?: string
  children: React.ReactNode
}

const ModalBody: React.FC<IModalBodyProps> = ({ children, className }) => (
  <div className={classNames("modal-body", className)}>{children}</div>
)

export default ModalBody
