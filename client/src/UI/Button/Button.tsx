import classNames from "classnames"
import React from "react"
import Icon from "../Icon"
import { IButtonProps } from "./Button.types"
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
  small,
  text,
  onClick,
}) => {
  return (
    <button
      className={classNames(
        "btn",
        { "btn-block": block, "btn-img": image, "btn-sm": small },
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
