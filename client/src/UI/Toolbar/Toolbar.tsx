import React from "react"
import Responsive from "../Responsive"

interface IToolbarProps {
  children: React.ReactNode
  desktop?: boolean
  tablet?: boolean
  mobile?: boolean
}

const Toolbar: React.FC<IToolbarProps> = ({
  children,
  desktop,
  tablet,
  mobile,
}) => (
  <Responsive
    className="toolbar"
    desktop={desktop}
    tablet={tablet}
    mobile={mobile}
  >
    <div className="row no-gutters">{children}</div>
  </Responsive>
)

export default Toolbar
