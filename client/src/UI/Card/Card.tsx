import classnames from "classnames"
import React from "react"

interface CardProps {
  className?: string
  children: React.ReactNode
}

const Card: React.FC<CardProps> = ({ children, className }) => (
  <div className={classnames("card-wrapper", className)}>
    <div className="card">{children}</div>
  </div>
)

export default Card
