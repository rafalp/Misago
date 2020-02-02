import classNames from "classnames"
import React from "react"
import Icon from "../Icon"
import { ButtonSpinner } from "../Button"

interface IDropdownButtonProps {
  className?: string | null
  disabled?: boolean
  icon?: string
  iconSolid?: boolean
  loading?: boolean
  text: React.ReactNode
  onClick?: () => void
}

const DropdownButton: React.FC<IDropdownButtonProps> = ({
  className,
  disabled,
  icon,
  iconSolid,
  loading,
  text,
  onClick,
}) => (
  <button
    className={classNames("dropdown-item", className)}
    disabled={disabled || loading}
    type="button"
    onClick={onClick}
  >
    {icon && !loading && <Icon icon={icon} solid={iconSolid} fixedWidth />}
    {loading && <ButtonSpinner />}
    <span>{text}</span>
  </button>
)

export default DropdownButton
