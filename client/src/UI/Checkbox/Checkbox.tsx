import React from "react"
import { useFormContext } from "react-hook-form"
import { useFieldContext } from "../Form"

interface ICheckboxProps {
  checked?: boolean
  disabled?: boolean
  id?: string
  name?: string
  required?: boolean
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void
}

const Checkbox: React.FC<ICheckboxProps> = ({
  checked,
  disabled,
  id,
  name,
  required,
  onChange,
}) => {
  const context = useFieldContext()
  const hookContext = useFormContext() || {}

  return (
    <span className="form-check-input">
      <input
        id={id || context.id}
        type="checkbox"
        checked={!!hookContext.register ? undefined : checked}
        disabled={disabled || context.disabled}
        name={name || context.name}
        ref={hookContext.register}
        required={required}
        onChange={onChange}
      />
    </span>
  )
}

export default Checkbox
