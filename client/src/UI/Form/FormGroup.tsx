import classNames from "classnames"
import React from "react"

interface IFormGroupProps {
  children?: React.ReactNode
  className?: string | null
}

const FormGroup: React.FC<IFormGroupProps> = ({ children, className }) => (
  <div className={classNames("form-group", className)}>{children}</div>
)

export default FormGroup