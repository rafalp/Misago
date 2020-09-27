import classnames from "classnames"
import React from "react"

interface ICardFormBodyProps {
  className?: string
  children: React.ReactNode
}

const CardFormBody: React.FC<ICardFormBodyProps> = ({
  children,
  className,
}) => (
  <div className={classnames("card-body", "card-form-body", className)}>
    {children}
  </div>
)

export default CardFormBody
