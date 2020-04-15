import classNames from "classnames"
import React from "react"

interface ITidbitItemProps {
  className?: string | null
  children?: React.ReactNode
}

const TidbitItem: React.FC<ITidbitItemProps> = ({ className, children }) => (
  <li className={classNames("list-inline-item", className)}>{children}</li>
)

export default TidbitItem
