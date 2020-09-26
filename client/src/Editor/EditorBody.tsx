import classnames from "classnames"
import React from "react"

interface IEditorBodyProps {
  children: React.ReactNode
  disabled?: boolean
}

const EditorBody: React.FC<IEditorBodyProps> = ({ children, disabled }) => (
  <div
    className={classnames("form-editor", {
      "form-editor-disabled": disabled,
    })}
  >
    {children}
  </div>
)

export default EditorBody
