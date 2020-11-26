import classnames from "classnames"
import React from "react"
import EditorMentions from "./EditorMentions"

interface IEditorTextareaProps {
  disabled?: boolean
  hidden?: boolean
  invalid?: boolean
  name: string
  register: (instance: HTMLTextAreaElement | undefined | null) => void
}

const EditorTextarea: React.FC<IEditorTextareaProps> = ({
  disabled,
  hidden,
  invalid,
  name,
  register,
}) => (
  <EditorMentions name={name}>
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
  </EditorMentions>
)

export default EditorTextarea
