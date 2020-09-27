import classnames from "classnames"
import React from "react"
import Icon from "../Icon"
import { Link } from "react-router-dom"

interface IDropdownLinkProps {
  className?: string | null
  icon?: string
  text: React.ReactNode
  to: string
  onClick?: (event: React.MouseEvent<HTMLAnchorElement, MouseEvent>) => void
}

const DropdownLink: React.FC<IDropdownLinkProps> = ({
  className,
  icon,
  text,
  to,
  onClick,
}) => (
  <Link
    className={classnames("dropdown-item", className)}
    to={to}
    onClick={onClick}
  >
    {icon && <Icon icon={icon} fixedWidth />}
    <span>{text}</span>
  </Link>
)

export default DropdownLink
