import classnames from "classnames"
import React from "react"

interface ICardListItemProps {
  children: React.ReactNode
  className?: string
}

const CardListItem: React.FC<ICardListItemProps> = ({
  children,
  className,
}) => <li className={classnames("list-group-item", className)}>{children}</li>

export default CardListItem
