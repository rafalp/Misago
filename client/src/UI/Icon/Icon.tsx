import classnames from "classnames"
import React from "react"

interface IconProps {
  fixedWidth?: boolean
  icon: string
}

const Icon: React.FC<IconProps> = ({ fixedWidth, icon }) => (
  <i className={classnames(icon, { "fa-fw": fixedWidth })} />
)

export default Icon
