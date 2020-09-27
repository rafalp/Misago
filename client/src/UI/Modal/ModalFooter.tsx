import classnames from "classnames"
import React from "react"

interface IModalFooterProps {
  className?: string
  children: React.ReactNode
}

const ModalFooter: React.FC<IModalFooterProps> = ({ children, className }) => (
  <div className={classnames("modal-footer", className)}>{children}</div>
)

export default ModalFooter
