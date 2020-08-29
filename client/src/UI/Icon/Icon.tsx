import classNames from "classnames"
import React from "react"

interface IIconProps {
  fixedWidth?: boolean
  icon: string
}

const Icon: React.FC<IIconProps> = ({ fixedWidth, icon }) => (
  <i className={classNames(icon, { "fa-fw": fixedWidth })} />
)

export default Icon
