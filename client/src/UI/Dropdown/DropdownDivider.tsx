import classnames from "classnames"
import React from "react"

interface IDropdownDividerProps {
  className?: string | null
}

const DropdownDivider: React.FC<IDropdownDividerProps> = ({ className }) => (
  <div className={classnames("dropdown-divider", className)} />
)

export default DropdownDivider
