import classnames from "classnames"
import React from "react"

interface EditorBodyProps {
  children: React.ReactNode
  disabled?: boolean
}

const EditorBody: React.FC<EditorBodyProps> = ({ children, disabled }) => (
  <div
    className={classnames("form-editor", {
      "form-editor-disabled": disabled,
    })}
  >
    {children}
  </div>
)

export default EditorBody
