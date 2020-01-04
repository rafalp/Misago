import React from "react"

interface ICardBodyProps {
  children?: React.ReactNode
}

const CardBody: React.FC<ICardBodyProps> = ({ children }) => (
  <div className="card-body">{children}</div>
)

export default CardBody
