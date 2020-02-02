import classNames from "classnames"
import React from "react"

interface IDropdownDividerProps {
  className?: string | null
}

const DropdownDivider: React.FC<IDropdownDividerProps> = ({ className }) => (
  <div className={classNames("dropdown-divider", className)} />
)

export default DropdownDivider
