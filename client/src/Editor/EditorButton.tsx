import classnames from "classnames"
import React from "react"
import Icon from "../UI/Icon"

interface EditorButtonProps {
  children?: React.ReactNode
  className?: string
  disabled?: boolean
  icon?: string
  title?: string
  onClick: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
}

const EditorButton: React.FC<EditorButtonProps> = ({
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
    {icon && <Icon icon={icon} fixedWidth />}
    {children}
  </button>
)

export default EditorButton
