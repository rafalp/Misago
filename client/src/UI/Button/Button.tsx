import classNames from "classnames"
import React from "react"
import Icon from "../Icon"
import { ButtonType } from "./Button.types"
import ButtonSpinner from "./ButtonSpinner"

interface IButtonProps {
  block?: boolean
  className?: string | null
  disabled?: boolean
  elementRef?: React.MutableRefObject<HTMLButtonElement>
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
  className,
  disabled,
  elementRef,
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
        { "btn-block": block },
        className
      )}
      ref={elementRef}
      type={onClick ? "button" : "submit"}
      disabled={disabled || loading}
      onClick={onClick}
    >
      {icon && !loading && <Icon icon={icon} solid={iconSolid} fixedWidth />}
      {loading && <ButtonSpinner />}
      {text && <span>{text}</span>}
    </button>
  )
}

export default Button
