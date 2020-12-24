import classnames from "classnames"
import React from "react"
import { useFormContext } from "react-hook-form"
import { useFieldContext } from "../Form"

interface TextareaProps {
  className?: string
  disabled?: boolean
  id?: string
  invalid?: boolean
  maxLength?: number
  name?: string
  placeholder?: string
  required?: boolean
  rows?: number
  onBlur?: (event: React.BaseSyntheticEvent<object, any, any>) => void
  onChange?: (event: React.BaseSyntheticEvent<object, any, any>) => void
}

const Textarea: React.FC<TextareaProps> = ({
  className,
  disabled,
  id,
  invalid,
  maxLength,
  name,
  placeholder,
  required,
  rows,
  onBlur,
  onChange,
}) => {
  const context = useFieldContext()
  const hookContext = useFormContext() || {}

  return (
    <textarea
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
      rows={rows || 5}
      onBlur={onBlur}
      onChange={onChange}
    />
  )
}

export default Textarea
