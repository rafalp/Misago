import classnames from "classnames"
import React from "react"

interface IEditorButtonProps {
  children: React.ReactNode
  className?: string
  disabled?: boolean
  icon?: boolean
  title?: string
  onClick?: () => void
}

const EditorButton: React.FC<IEditorButtonProps> = ({
  children,
  className,
  disabled,
  icon,
  title,
  onClick,
}) => (
  <button
    className={classnames(
      "btn btn-outline-secondary btn-editor btn-sm",
      className,
      {
        "btn-icon": icon,
      }
    )}
    title={title}
    type="button"
    disabled={disabled}
    onClick={onClick}
  >
    {children}
  </button>
)

export default EditorButton
