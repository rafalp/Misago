import classnames from "classnames"
import React from "react"
import Responsive from "../Responsive"

interface ToolbarItemProps {
  children: React.ReactNode
  fill?: boolean
  desktop?: boolean
  tablet?: boolean
  mobile?: boolean
  landscape?: boolean
  portrait?: boolean
}

const ToolbarItem: React.FC<ToolbarItemProps> = ({
  children,
  fill,
  desktop,
  tablet,
  mobile,
  landscape,
  portrait,
}) => (
  <Responsive
    className={classnames("toolbar-item", fill ? "col" : "col-auto")}
    desktop={desktop}
    tablet={tablet}
    mobile={mobile}
    landscape={landscape}
    portrait={portrait}
  >
    {children}
  </Responsive>
)

export default ToolbarItem
