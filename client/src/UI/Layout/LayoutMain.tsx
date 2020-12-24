import classnames from "classnames"
import React from "react"

interface LayoutMainProps {
  className?: string
  children?: React.ReactNode
}

const LayoutMain: React.FC<LayoutMainProps> = ({ className, children }) => (
  <div className={classnames("col col-main", className)}>{children}</div>
)

export default LayoutMain
