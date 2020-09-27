import classnames from "classnames"
import React from "react"

interface ILayoutMainProps {
  className?: string
  children?: React.ReactNode
}

const LayoutMain: React.FC<ILayoutMainProps> = ({ className, children }) => (
  <div className={classnames("col col-main", className)}>{children}</div>
)

export default LayoutMain
