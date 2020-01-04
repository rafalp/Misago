import classNames from "classnames"
import React from "react"

interface ICardProps {
  className?: string
  children: React.ReactNode
}

const Card: React.FC<ICardProps> = ({ children, className }) => (
  <div className={classNames("card-wrapper", className)}>
    <div className="card">{children}</div>
  </div>
)

export default Card
