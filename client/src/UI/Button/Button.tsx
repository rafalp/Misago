import classNames from "classnames"
import React from "react"
import Icon from "../Icon"

interface IButtonProps {
  icon?: string
  iconSolid?: boolean
  text?: string
  type?: string
  outline?: boolean
}

const Button: React.FC<IButtonProps> = ({ icon, iconSolid, text, type="primary", outline }) => {
  return (
    <button className={classNames("btn", outline ? `btn-outline-${type}` : `btn-${type}`)}>
      {icon && <Icon icon={icon} solid={iconSolid} fixedWidth />}
      {text && <span>{text}</span>}
    </button>
  )
}

export default Button