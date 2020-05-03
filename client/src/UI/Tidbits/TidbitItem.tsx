import classNames from "classnames"
import React from "react"

interface ITidbitItemProps {
  className?: string | null
  children?: React.ReactNode
  title?: string
}

const TidbitItem: React.FC<ITidbitItemProps> = ({
  className,
  children,
  title,
}) => (
  <li className={classNames("list-inline-item", className)} title={title}>
    {children}
  </li>
)

export default TidbitItem
