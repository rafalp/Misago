import React from "react"

interface IAppContainerProps {
  children: React.ReactNode
}

const AppContainer: React.FC<IAppContainerProps> = ({ children }) => {
  return <div className="app-container">{children}</div>
}

export default AppContainer
