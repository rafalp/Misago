import classnames from "classnames"
import React from "react"

interface ICardBodyProps {
  children?: React.ReactNode
  className?: string
}

const CardBody: React.FC<ICardBodyProps> = ({ children, className }) => (
  <div className={classnames("card-body", className)}>{children}</div>
)

export default CardBody
