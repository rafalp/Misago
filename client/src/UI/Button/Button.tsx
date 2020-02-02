import classNames from "classnames"
import React from "react"
import Icon from "../Icon"
import { ButtonType } from "./Button.types"
import ButtonSpinner from "./ButtonSpinner"

interface IButtonProps {
  block?: boolean
  className?: string | null
  disabled?: boolean
  elementRef?: React.MutableRefObject<HTMLButtonElement | null>
  icon?: string
  iconSolid?: boolean
  image?: React.ReactNode
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
  image,
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
        { "btn-img": image },
        className
      )}
      ref={elementRef}
      type={onClick ? "button" : "submit"}
      disabled={disabled || loading}
      onClick={onClick}
    >
      {icon && !loading && <Icon icon={icon} solid={iconSolid} fixedWidth />}
      {!loading && image}
      {loading && <ButtonSpinner />}
      {text && <span>{text}</span>}
    </button>
  )
}

export default Button
