import classNames from "classnames"
import React from "react"

interface ICardFormBodyProps {
  className?: string
  children: React.ReactNode
}

const CardFormBody: React.FC<ICardFormBodyProps> = ({
  children,
  className,
}) => (
  <div className={classNames("modal-body", "modal-form-body", className)}>
    {children}
  </div>
)

export default CardFormBody
