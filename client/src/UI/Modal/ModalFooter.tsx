import classnames from "classnames"
import React from "react"

interface ModalFooterProps {
  className?: string
  children: React.ReactNode
}

const ModalFooter: React.FC<ModalFooterProps> = ({ children, className }) => (
  <div className={classnames("modal-footer", className)}>{children}</div>
)

export default ModalFooter
