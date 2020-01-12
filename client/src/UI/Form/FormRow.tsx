import React from "react"

interface IFormRowProps {
  children?: React.ReactNode
}

const FormRow: React.FC<IFormRowProps> = ({ children }) => (
  <div className="form-row">{children}</div>
)

export default FormRow