import React from "react"

interface TidbitNumberProps {
  children: React.ReactNode
}

const TidbitNumber: React.FC<TidbitNumberProps> = ({ children }) => (
  <span className="tidbit-number">{children}</span>
)

export default TidbitNumber
