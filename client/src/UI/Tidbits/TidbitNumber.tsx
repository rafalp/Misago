import React from "react"

interface ITidbitNumberProps {
  children: React.ReactNode
}

const TidbitNumber: React.FC<ITidbitNumberProps> = ({ children }) => (
  <span className="tidbit-number">{children}</span>
)

export default TidbitNumber
