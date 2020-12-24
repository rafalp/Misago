import classnames from "classnames"
import React from "react"

interface ModalBodyProps {
  className?: string
  children: React.ReactNode
}

const ModalBody: React.FC<ModalBodyProps> = ({ children, className }) => (
  <div className={classnames("modal-body", className)}>{children}</div>
)

export default ModalBody
