import React from "react"
import { useFormContext } from "react-hook-form"
import classnames from "classnames"
import { FieldContext } from "./FieldContext"
import { FieldLabel } from "./FieldLabel"
import { FormContext } from "./FormContext"

interface FieldProps {
  check?: boolean
  className?: string
  disabled?: boolean
  error?: (
    error: { type: string; message: string },
    value: any
  ) => React.ReactNode
  id?: string
  input?: React.ReactNode
  label?: React.ReactNode
  labelReaderOnly?: React.ReactNode
  name?: string
  required?: boolean
}

const Field: React.FC<FieldProps> = ({
  check,
  className,
  disabled,
  error,
  id,
  input,
  label,
  labelReaderOnly,
  name,
  required,
}) => {
  const { disabled: formDisabled, id: formId } = React.useContext(FormContext)
  const fieldId = getFieldId(formId, id, name)

  const { errors, getValues } = useFormContext()
  const fieldError = name ? errors[name] : undefined
  const fieldValue = name ? getValues()[name] : undefined

  return (
    <FieldContext.Provider
      value={{
        disabled: disabled || formDisabled,
        id: fieldId,
        invalid: !!fieldError,
        name: name,
        required: required,
      }}
    >
      <div className={classnames("form-group", className)}>
        {check ? (
          <div className="form-check">
            {input}
            {label && (
              <FieldLabel
                className="form-check-label"
                htmlFor={fieldId}
                required={required}
              >
                {label}
              </FieldLabel>
            )}
          </div>
        ) : (
          <>
            {label && (
              <FieldLabel
                htmlFor={fieldId}
                readerOnly={labelReaderOnly}
                required={required}
              >
                {label}
              </FieldLabel>
            )}
            {input}
          </>
        )}
        {error && fieldError && error(fieldError, fieldValue)}
      </div>
    </FieldContext.Provider>
  )
}

const getFieldId = (formId?: string, id?: string, name?: string) => {
  if (!id && !name) return undefined
  if (formId) return `${formId}_${id || name}`
  return id || name
}

export default Field
