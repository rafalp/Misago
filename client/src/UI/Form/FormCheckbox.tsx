import React from "react"

interface IFormCheckboxProps {
  children: React.ReactNode
}

const FormCheckbox: React.FC<IFormCheckboxProps> = ({ children }) => (
  <div className="form-check">{children}</div>
)

export default FormCheckbox
