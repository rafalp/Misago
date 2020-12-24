import React from "react"

interface CardHeaderProps {
  title: React.ReactNode
}

const CardHeader: React.FC<CardHeaderProps> = ({ title }) => (
  <h5 className="card-header">{title}</h5>
)

export default CardHeader
