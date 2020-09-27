import classnames from "classnames"
import React from "react"
import { Link } from "react-router-dom"
import Icon from "../Icon"

interface ISideNavItemProps {
  className?: string | null
  children: React.ReactNode
  hasChildren?: boolean
  icon?: React.ReactNode
  isActive?: boolean
  isChild?: boolean
  to: string
}

const SideNavItem: React.FC<ISideNavItemProps> = ({
  className,
  children,
  hasChildren,
  icon,
  isActive,
  isChild,
  to,
}) => (
  <li className="nav-item">
    <Link
      aria-selected={isActive ? "true" : "false"}
      className={classnames(
        "nav-link",
        {
          "nav-link-child": isChild,
          active: isActive,
        },
        className
      )}
      to={to}
    >
      {icon && <span className="nav-link-icon">{icon}</span>}
      <span className="nav-link-text">{children}</span>
      {hasChildren && <HasChildrenIcon />}
    </Link>
  </li>
)

const HasChildrenIcon: React.FC = () => (
  <span className="has-children-icon">
    <Icon icon="far fa-plus-square" />
  </span>
)

export default SideNavItem
