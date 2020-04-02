import classNames from "classnames"
import React from "react"
import { useFormContext } from "react-hook-form"
import { FieldContext } from "../Form"

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
  onBlur,
  onChange,
}) => {
  const context = React.useContext(FieldContext)
  const hookContext = useFormContext() || {}

  return (
    <input
      className={classNames(
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
      onBlur={onBlur}
      onChange={onChange}
    />
  )
}

export default Input
