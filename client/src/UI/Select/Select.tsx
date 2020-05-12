import classNames from "classnames"
import React from "react"
import { useFormContext } from "react-hook-form"
import { FieldContext } from "../Form"

interface ISelectProps {
  className?: string
  disabled?: boolean
  id?: string
  invalid?: boolean
  name?: string
  options: Array<IISelectOption>
  placeholder?: string
  required?: boolean
  onBlur?: (event: React.BaseSyntheticEvent<object, any, any>) => void
  onChange?: (event: React.BaseSyntheticEvent<object, any, any>) => void
}

interface IISelectOption {
  name: React.ReactNode
  value: string | number
}

const Select: React.FC<ISelectProps> = ({
  className,
  disabled,
  id,
  invalid,
  name,
  options,
  placeholder,
  required,
  onBlur,
  onChange,
}) => {
  const context = React.useContext(FieldContext)
  const hookContext = useFormContext() || {}

  return (
    <select
      className={classNames(
        "form-control",
        { "is-invalid": invalid || context.invalid },
        className
      )}
      disabled={disabled || context.disabled}
      id={id || context.id}
      name={name || context.name}
      placeholder={placeholder}
      ref={hookContext.register}
      required={required || context.required}
      onBlur={onBlur}
      onChange={onChange}
    >
      {options.map(({ name, value }) => (
        <option key={value} value={value}>
          {name}
        </option>
      ))}
    </select>
  )
}

export default Select
