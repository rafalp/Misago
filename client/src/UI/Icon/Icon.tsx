import classNames from "classnames"
import React from "react"

interface IIconProps {
  fixedWidth?: boolean
  icon: string
  solid?: boolean
}

const Icon: React.FC<IIconProps> = ({ fixedWidth, icon, solid }) => (
  <i
    className={classNames(solid ? "fas" : "far", `fa-${icon}`, {
      "fa-fw": fixedWidth,
    })}
  />
)

export default Icon
