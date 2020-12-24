import React from "react"

interface LayoutProps {
  children?: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => (
  <div className="row">{children}</div>
)

export default Layout
