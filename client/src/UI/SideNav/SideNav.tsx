import classNames from "classnames"
import React from "react"

interface ISideNavProps {
  className?: string | null
  children: React.ReactNode
}

const SideNav: React.FC<ISideNavProps> = ({ className, children }) => (
  <ul className={classNames("nav nav-side flex-column", className)}>
    {children}
  </ul>
)

export default SideNav
