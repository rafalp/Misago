import React from "react"
import Responsive from "../Responsive"

interface IToolbarProps {
  children: React.ReactNode
  desktop?: boolean
  tablet?: boolean
  mobile?: boolean
  landscape?: boolean
  portrait?: boolean
}

const Toolbar: React.FC<IToolbarProps> = ({
  children,
  desktop,
  tablet,
  mobile,
  landscape,
  portrait,
}) => (
  <Responsive
    className="toolbar"
    desktop={desktop}
    tablet={tablet}
    mobile={mobile}
    landscape={landscape}
    portrait={portrait}
  >
    <div className="row align-items-center no-gutters">{children}</div>
  </Responsive>
)

export default Toolbar
