import React from "react"

interface ICardHeaderProps {
  title: React.ReactNode
}

const CardHeader: React.FC<ICardHeaderProps> = ({ title }) => (
  <h5 className="card-header">{title}</h5>
)

export default CardHeader
