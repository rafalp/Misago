import classnames from "classnames"
import React from "react"

interface LayoutSideProps {
  className?: string
  children?: React.ReactNode
}

const LayoutSide: React.FC<LayoutSideProps> = ({ className, children }) => (
  <div className={classnames("col col-side", className)}>{children}</div>
)

export default LayoutSide
