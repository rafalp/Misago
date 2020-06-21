import React from "react"

interface IDropdownHeaderProps {
  text: React.ReactNode
}

const DropdownHeader: React.FC<IDropdownHeaderProps> = ({ text }) => (
  <h6 className="dropdown-header">{text}</h6>
)

export default DropdownHeader
