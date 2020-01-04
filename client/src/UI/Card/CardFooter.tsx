import React from "react"

interface ICardFooterProps {
  children?: React.ReactNode
}

const CardFooter: React.FC<ICardFooterProps> = ({ children }) => (
  <div className="card-footer">{children}</div>
)

export default CardFooter
