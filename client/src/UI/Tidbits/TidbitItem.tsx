import classnames from "classnames"
import React from "react"

interface TidbitItemProps {
  className?: string | null
  children?: React.ReactNode
  title?: string
}

const TidbitItem: React.FC<TidbitItemProps> = ({
  className,
  children,
  title,
}) => (
  <li
    className={classnames("list-inline-item tidbit-item", className)}
    title={title}
  >
    {children}
  </li>
)

export default TidbitItem
