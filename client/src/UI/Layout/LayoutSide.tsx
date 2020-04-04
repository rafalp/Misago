import classNames from "classnames"
import React from "react"

interface ILayoutSideProps {
  className?: string
  children?: React.ReactNode
}

const LayoutSide: React.FC<ILayoutSideProps> = ({ className, children }) => (
  <div className={classNames("col col-side", className)}>{children}</div>
)

export default LayoutSide
