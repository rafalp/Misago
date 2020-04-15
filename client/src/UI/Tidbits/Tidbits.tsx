import React from "react"

interface ITidbitsProps {
  children?: React.ReactNode
}

const Tidbits: React.FC<ITidbitsProps> = ({ children }) => (
  <ul className="list-inline list-tidbits">{children}</ul>
)

export default Tidbits
