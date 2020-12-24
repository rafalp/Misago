import React from "react"

interface DropdownHeaderProps {
  text: React.ReactNode
}

const DropdownHeader: React.FC<DropdownHeaderProps> = ({ text }) => (
  <h6 className="dropdown-header">{text}</h6>
)

export default DropdownHeader
