import { useField, useFormikContext } from "formik"
import React from "react"
import { FormFieldContext } from "../../Context"
import { FieldLabel } from "../Field"
import FormGroup from "./FormGroup"

interface IFormFieldProps {
  error: (error: string | null | undefined, value: any) => React.ReactNode
  input: React.ReactNode
  id: string
  label: React.ReactNode
  name: string
}

const FormField: React.FC<IFormFieldProps> = ({ id, input, label, name, error }) => {
  const { isSubmitting: disabled } = useFormikContext()
  const [{ value, onBlur, onChange }, { error: fieldError, touched }] = useField(name)

  return (
    <FormFieldContext.Provider
      value={{ id, name, disabled, value, onBlur, onChange, valid: touched && fieldError ? false : null }}
    >
      <FormGroup>
        <FieldLabel htmlFor={id}>{label}</FieldLabel>
        {input}
        {fieldError && error(fieldError, value)}
      </FormGroup>
    </FormFieldContext.Provider>
  )
}

export default FormField
