import React from "react"
import EditorButton from "../EditorButton"

interface EditorControlButtonProps {
  disabled?: boolean
  icon: string
  title: string
  name: string
  onClick: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
}

const EditorControlButton: React.FC<EditorControlButtonProps> = ({
  disabled,
  icon,
  title,
  name,
  onClick,
}) => (
  <EditorButton
    className={"btn-editor-" + name}
    disabled={disabled}
    icon={icon}
    title={title}
    onClick={onClick}
  />
)

export default EditorControlButton
