import classnames from "classnames"
import React from "react"
import { useFormContext } from "react-hook-form"
import { useFieldContext } from "../Form"

interface IInputProps {
  className?: string
  disabled?: boolean
  id?: string
  invalid?: boolean
  maxLength?: number
  name?: string
  placeholder?: string
  required?: boolean
  type?: "text" | "email" | "password"
  value?: string
  onBlur?: (event: React.BaseSyntheticEvent<object, any, any>) => void
  onChange?: (event: React.BaseSyntheticEvent<object, any, any>) => void
}

const Input: React.FC<IInputProps> = ({
  className,
  disabled,
  id,
  invalid,
  maxLength,
  name,
  placeholder,
  required,
  type,
  value,
  onBlur,
  onChange,
}) => {
  const context = useFieldContext()
  const hookContext = useFormContext() || {}

  return (
    <input
      className={classnames(
        "form-control",
        { "is-invalid": invalid || context.invalid },
        className
      )}
      disabled={disabled || context.disabled}
      id={id || context.id}
      maxLength={maxLength}
      name={name || context.name}
      placeholder={placeholder}
      ref={hookContext.register}
      required={required || context.required}
      type={type || "text"}
      value={value}
      onBlur={onBlur}
      onChange={onChange}
    />
  )
}

export default Input
