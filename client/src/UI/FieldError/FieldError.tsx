import React from "react"

interface IFieldErrorProps {
  children?: React.ReactNode
}

const FieldError: React.FC<IFieldErrorProps> = ({ children }) => (
  <div className="invalid-feedback">{children}</div>
)

export default FieldError
