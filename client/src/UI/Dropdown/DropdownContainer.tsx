import React from "react"

interface IDropdownContainerProps {
  children: React.ReactNode
}

const DropdownContainer: React.FC<IDropdownContainerProps> = ({ children }) => (
  <div className="dropdown-container">{children}</div>
)

export default DropdownContainer
