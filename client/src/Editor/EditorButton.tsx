import React from "react"

interface IEditorButtonProps {
  children: React.ReactNode
  disabled?: boolean
  onClick?: () => void
}

const EditorButton: React.FC<IEditorButtonProps> = ({
  children,
  disabled,
  onClick,
}) => (
  <button
    className="btn btn-outline-secondary btn-editor btn-sm"
    type="button"
    disabled={disabled}
    onClick={onClick}
  >
    {children}
  </button>
)

export default EditorButton
