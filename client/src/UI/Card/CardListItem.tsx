import classnames from "classnames"
import React from "react"

interface CardListItemProps {
  children: React.ReactNode
  className?: string
}

const CardListItem: React.FC<CardListItemProps> = ({
  children,
  className,
}) => <li className={classnames("list-group-item", className)}>{children}</li>

export default CardListItem
