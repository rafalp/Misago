import classNames from "classnames"
import React from "react"
import { Link } from "react-router-dom"

interface IDropdownLinkProps {
  children: React.ReactNode
  className?: string | null
  to: string
}

const DropdownLink: React.FC<IDropdownLinkProps> = ({
  children,
  className,
  to,
}) => (
  <Link className={classNames("dropdown-item", className)} to={to}>
    {children}
  </Link>
)

export default DropdownLink
