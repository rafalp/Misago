import classnames from "classnames"
import React from "react"
import Icon from "../Icon"
import { ButtonSpinner } from "../Button"

interface IDropdownButtonProps {
  className?: string | null
  disabled?: boolean
  icon?: string
  loading?: boolean
  text: React.ReactNode
  onClick?: () => void
}

const DropdownButton: React.FC<IDropdownButtonProps> = ({
  className,
  disabled,
  icon,
  loading,
  text,
  onClick,
}) => (
  <button
    className={classnames("dropdown-item", className)}
    disabled={disabled || loading}
    type="button"
    onClick={onClick}
  >
    {icon && !loading && <Icon icon={icon} fixedWidth />}
    {loading && <ButtonSpinner />}
    <span>{text}</span>
  </button>
)

export default DropdownButton
