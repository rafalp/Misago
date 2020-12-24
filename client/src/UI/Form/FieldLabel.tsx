import classnames from "classnames"
import React from "react"

interface FieldLabelProps {
  children?: React.ReactNode
  className?: string
  htmlFor?: string
  readerOnly?: React.ReactNode
  required?: boolean
}

const FieldLabel: React.FC<FieldLabelProps> = ({
  children,
  className,
  htmlFor,
  readerOnly,
  required,
}) => (
  <label
    className={classnames(className, { "sr-only": readerOnly }) || undefined}
    htmlFor={htmlFor}
  >
    {children}
    {required && <FieldRequired />}
  </label>
)

const FieldRequired: React.FC = () => <span className="field-required">*</span>

export { FieldLabel, FieldRequired }
