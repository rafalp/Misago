import classnames from "classnames"
import React from "react"

interface CardFooterProps {
  className?: string
  children?: React.ReactNode
}

const CardFooter: React.FC<CardFooterProps> = ({ className, children }) => (
  <div className={classnames("card-footer", className)}>{children}</div>
)

export default CardFooter
