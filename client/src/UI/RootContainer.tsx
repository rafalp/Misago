import React from "react"

interface IRootContainerProps {
  children: React.ReactNode
}

const RootContainer: React.FC<IRootContainerProps> = ({ children }) => {
  return <div className="root-container">{children}</div>
}

export default RootContainer
