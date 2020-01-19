import classNames from "classnames"
import React from "react"
import Icon from "../Icon"
import { ButtonType } from "./Button.types"

interface IButtonProps {
  block?: boolean
  disabled?: boolean
  icon?: string
  iconSolid?: boolean
  loading?: boolean
  text?: React.ReactNode
  type?: ButtonType
  outline?: boolean
  onClick?: () => void
}

const Button: React.FC<IButtonProps> = ({
  block,
  disabled,
  icon,
  iconSolid,
  loading,
  text,
  type = ButtonType.PRIMARY,
  outline,
  onClick,
}) => {
  return (
    <button
      className={classNames(
        "btn",
        outline ? `btn-outline-${type}` : `btn-${type}`,
        { "btn-block": block }
      )}
      type={onClick ? "button" : "submit"}
      disabled={disabled}
      onClick={onClick}
    >
      {icon && !loading && <Icon icon={icon} solid={iconSolid} fixedWidth />}
      {loading && <ButtonSpinner />}
      {text && <span>{text}</span>}
    </button>
  )
}

const ButtonSpinner: React.FC = () => (
  <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true" />
)

export default Button
