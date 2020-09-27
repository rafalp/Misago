import classnames from "classnames"
import React from "react"

interface ICardFooterProps {
  className?: string
  children?: React.ReactNode
}

const CardFooter: React.FC<ICardFooterProps> = ({ className, children }) => (
  <div className={classnames("card-footer", className)}>{children}</div>
)

export default CardFooter
