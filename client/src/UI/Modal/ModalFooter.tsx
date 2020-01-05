import classNames from "classnames"
import React from "react"

interface IModalFooterProps {
  className?: string
  children: React.ReactNode
}

const ModalFooter: React.FC<IModalFooterProps> = ({ children, className }) => (
  <div className={classNames("modal-footer", className)}>{children}</div>
)

export default ModalFooter
