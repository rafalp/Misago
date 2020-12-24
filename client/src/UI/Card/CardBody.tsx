import classnames from "classnames"
import React from "react"

interface CardBodyProps {
  children?: React.ReactNode
  className?: string
}

const CardBody: React.FC<CardBodyProps> = ({ children, className }) => (
  <div className={classnames("card-body", className)}>{children}</div>
)

export default CardBody
