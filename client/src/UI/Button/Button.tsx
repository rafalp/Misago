import classNames from "classnames"
import React from "react"
import Icon from "../Icon"

interface IButtonProps {
  icon?: string
  iconSolid?: boolean
  text?: React.ReactNode
  type?: string
  outline?: boolean
  onClick?: () => void
}

const Button: React.FC<IButtonProps> = ({
  icon,
  iconSolid,
  text,
  type = "primary",
  outline,
  onClick,
}) => {
  return (
    <button
      className={classNames("btn", outline ? `btn-outline-${type}` : `btn-${type}`)}
      type={onClick ? "button" : "submit"}
      onClick={onClick}
    >
      {icon && <Icon icon={icon} solid={iconSolid} fixedWidth />}
      {text && <span>{text}</span>}
    </button>
  )
}

export default Button
