import classnames from "classnames"
import React from "react"

interface IEditorTextareaProps {
  disabled?: boolean
  hidden?: boolean
  invalid?: boolean
  name: string
  register?: (instance: HTMLTextAreaElement | undefined | null) => void
}

const EditorTextarea: React.FC<IEditorTextareaProps> = ({
  disabled,
  hidden,
  invalid,
  name,
  register,
}) => (
  <textarea
    className={classnames(
      "form-control form-control-responsive form-editor-textarea",
      {
        "d-none": hidden,
        "is-invalid": invalid,
      }
    )}
    disabled={disabled}
    name={name}
    ref={register}
  />
)

export default EditorTextarea
