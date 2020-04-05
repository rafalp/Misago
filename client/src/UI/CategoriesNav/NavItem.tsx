import React from "react"
import classNames from "classnames"
import { Link } from "react-router-dom"
import * as urls from "../../urls"
import Icon from "../Icon"
import { IChild } from "./CategoriesNav.types"

interface INavItemProps {
  category: IChild
  isActive: boolean
  isChild?: boolean
  hasChildren?: boolean
}

const NavItem: React.FC<INavItemProps> = ({
  category,
  isActive,
  isChild,
  hasChildren,
}) => (
  <li className="nav-item">
    <Link
      aria-selected={isActive ? "true" : "false"}
      className={classNames("nav-link", {
        "nav-link-child": isChild,
        active: isActive,
      })}
      to={urls.category(category)}
    >
      <NavItemIcon color={category.color} isActive={isActive} />
      <span className="nav-link-title">{category.name}</span>
      {hasChildren && <HasChildrenIcon />}
    </Link>
  </li>
)

interface INavItemIconProps {
  color?: string
  isActive: boolean
}

const NavItemIcon: React.FC<INavItemIconProps> = ({ color, isActive }) => (
  <span
    className="nav-link-icon"
    style={
      color ? (isActive ? { background: color } : { color: color }) : undefined
    }
  >
    <Icon icon="comment-alt" fixedWidth />
  </span>
)

const HasChildrenIcon: React.FC = () => (
  <div className="has-more">
    <Icon icon="plus-square" />
  </div>
)

export default NavItem

export { NavItemIcon, HasChildrenIcon }
