import classNames from "classnames"
import React from "react"
import { useFormContext } from "react-hook-form"
import { useFieldContext } from "../UI/Form"

interface IEditorProps {
  name?: string
  disabled?: boolean
}

const Editor: React.FC<IEditorProps> = ({ name, disabled }) => {
  const context = useFieldContext()
  const hookContext = useFormContext() || {}

  return (
    <textarea
      className={classNames("form-control", { "is-invalid": context.invalid })}
      disabled={disabled || context.disabled}
      name={name || context.name}
      ref={hookContext.register}
      rows={5}
    />
  )
}

export default Editor
