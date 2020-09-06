import React from "react"

interface IFieldLabelProps {
  children?: React.ReactNode
  htmlFor?: string
  readerOnly?: React.ReactNode
  required?: boolean
}

const FieldLabel: React.FC<IFieldLabelProps> = ({
  children,
  htmlFor,
  readerOnly,
  required,
}) => (
  <label className={readerOnly ? "sr-only" : undefined} htmlFor={htmlFor}>
    {children}
    {required && <FieldRequired />}
  </label>
)

const FieldRequired: React.FC = () => <span className="field-required">*</span>

export { FieldLabel, FieldRequired }
