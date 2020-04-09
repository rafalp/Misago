import React from "react"

interface IMobileOnly {
  children: React.ReactNode
}

const MobileOnly: React.FC<IMobileOnly> = ({ children }) => (
  <div className="d-md-none mb-3">
    {children}
  </div>
)

export default MobileOnly