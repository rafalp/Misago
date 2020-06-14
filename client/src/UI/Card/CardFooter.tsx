import classNames from "classnames"
import React from "react"

interface ICardFooterProps {
  className?: string
  children?: React.ReactNode
}

const CardFooter: React.FC<ICardFooterProps> = ({ className, children }) => (
  <div className={classNames("card-footer", className)}>{children}</div>
)

export default CardFooter
