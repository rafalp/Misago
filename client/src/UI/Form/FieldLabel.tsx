import React from "react"

interface IFieldLabelProps {
  children?: React.ReactNode
  htmlFor?: string
  required?: boolean
}

const FieldLabel: React.FC<IFieldLabelProps> = ({
  children,
  htmlFor,
  required,
}) => (
  <label htmlFor={htmlFor}>
    {children}
    {required && <FieldRequired />}
  </label>
)

const FieldRequired: React.FC = () => <span className="field-required">*</span>

export { FieldLabel, FieldRequired }
