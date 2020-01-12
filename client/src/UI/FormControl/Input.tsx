import classNames from "classnames"
import React from "react"
import { FormFieldContext } from "../../Context"

interface IInputProps {
  className?: string
  defaultValue?: string
  disabled?: boolean
  id?: string
  maxLength?: number
  minLength?: number
  name?: string
  placeholder?: string
  ref?: React.RefObject<HTMLInputElement>
  required?: boolean
  type?: "text" | "email" | "password"
  valid?: boolean | null
  value?: string
  onBlur?: React.ChangeEventHandler<HTMLInputElement>
  onChange?: React.ChangeEventHandler<HTMLInputElement>
}

const Input: React.FC<IInputProps> = ({
  className,
  defaultValue,
  disabled,
  id,
  maxLength,
  minLength,
  name,
  placeholder,
  ref,
  required,
  type = "text",
  valid,
  value,
  onBlur,
  onChange,
}) => (
  <FormFieldContext.Consumer>
    {context => (
      <input
        className={classNames(
          "form-control",
          {
            "is-valid": (valid || context?.valid) === true,
            "is-invalid": (valid || context?.valid) === false,
          },
          className
        )}
        defaultValue={defaultValue}
        disabled={disabled || context?.disabled}
        id={id || context?.id}
        maxLength={maxLength}
        minLength={minLength}
        name={name || context?.name}
        placeholder={placeholder}
        ref={ref}
        required={required}
        type={type}
        value={value || context?.value}
        onBlur={onBlur || context?.onBlur}
        onChange={onChange || context?.onChange}
      />
    )}
  </FormFieldContext.Consumer>
)

export default Input
