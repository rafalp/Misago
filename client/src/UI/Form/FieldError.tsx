import React from "react"

interface FieldErrorProps {
  children?: React.ReactNode
}

const FieldError: React.FC<FieldErrorProps> = ({ children }) => (
  <div className="invalid-feedback">{children}</div>
)

export default FieldError
