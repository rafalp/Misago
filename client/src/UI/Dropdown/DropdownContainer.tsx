import React from "react"

interface DropdownContainerProps {
  children: React.ReactNode
}

const DropdownContainer: React.FC<DropdownContainerProps> = ({
  children,
}) => <div className="dropdown-container">{children}</div>

export default DropdownContainer
