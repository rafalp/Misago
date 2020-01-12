import React from "react"

interface IFormFieldContext {
  id: string
  name: string
  disabled: boolean
  valid: boolean | null
  value: any
  onBlur: React.ChangeEventHandler<HTMLInputElement>
  onChange: React.ChangeEventHandler<HTMLInputElement>
}

const FormFieldContext = React.createContext<IFormFieldContext | null>(null)

export default FormFieldContext
