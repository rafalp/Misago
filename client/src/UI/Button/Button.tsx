import classNames from "classnames"
import React from "react"
import Icon from "../Icon"
import { ButtonType, IButtonProps } from "./Button.types"
import ButtonSpinner from "./ButtonSpinner"

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
