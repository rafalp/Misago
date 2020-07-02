import classNames from "classnames"
import React from "react"
import Responsive from "../Responsive"

interface IToolbarItemProps {
  children: React.ReactNode
  fill?: boolean
  desktop?: boolean
  tablet?: boolean
  mobile?: boolean
  landscape?: boolean
  portrait?: boolean
}

const ToolbarItem: React.FC<IToolbarItemProps> = ({
  children,
  fill,
  desktop,
  tablet,
  mobile,
  landscape,
  portrait,
}) => (
  <Responsive
    className={classNames("toolbar-item", fill ? "col" : "col-auto")}
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
