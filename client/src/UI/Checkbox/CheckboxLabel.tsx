import React from "react"
import { FieldRequired } from "../Form"

interface ICheckboxLabelProps {
  children?: React.ReactNode
  htmlFor?: string
  required?: boolean
}

const CheckboxLabel: React.FC<ICheckboxLabelProps> = ({
  children,
  htmlFor,
  required,
}) => (
  <label className="form-check-label" htmlFor={htmlFor}>
    {children}
    {required && <FieldRequired />}
  </label>
)

export default CheckboxLabel
