import React from "react"

interface IFieldLabelProps {
  htmlFor?: string
  children?: React.ReactNode
}

const FieldLabel: React.FC<IFieldLabelProps> = ({ children, htmlFor }) => (
  <label htmlFor={htmlFor}>{children}</label>
)

export default FieldLabel
