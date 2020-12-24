import classnames from "classnames"
import React from "react"

interface DropdownDividerProps {
  className?: string | null
}

const DropdownDivider: React.FC<DropdownDividerProps> = ({ className }) => (
  <div className={classnames("dropdown-divider", className)} />
)

export default DropdownDivider
