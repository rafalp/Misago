import classNames from "classnames"
import React from "react"
import Icon from "../Icon"
import { Link } from "react-router-dom"

interface IDropdownLinkProps {
  children: React.ReactNode
  className?: string | null
  icon?: string
  iconSolid?: boolean
  to: string
  onClick?: (event: React.MouseEvent<HTMLAnchorElement, MouseEvent>) => void
}

const DropdownLink: React.FC<IDropdownLinkProps> = ({
  children,
  className,
  icon,
  iconSolid,
  to,
  onClick,
}) => (
  <Link
    className={classNames("dropdown-item", className)}
    to={to}
    onClick={onClick}
  >
    {icon && <Icon icon={icon} solid={iconSolid} fixedWidth />}
    <span>{children}</span>
  </Link>
)

export default DropdownLink
