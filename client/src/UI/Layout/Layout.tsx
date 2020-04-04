import React from "react"

interface ILayoutProps {
  children?: React.ReactNode
}

const Layout: React.FC<ILayoutProps> = ({ children }) => (
  <div className="row">{children}</div>
)

export default Layout
