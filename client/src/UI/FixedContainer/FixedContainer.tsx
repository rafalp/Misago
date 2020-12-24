import classnames from "classnames"
import React from "react"

interface FixedContainerProps {
  children: React.ReactNode
  className?: string
  show?: boolean
}

const FixedContainer: React.FC<FixedContainerProps> = ({
  children,
  className,
  show,
}) => (
  <div className={classnames("fixed-container", { show: show }, className)}>
    <div className="container-fluid">{children}</div>
  </div>
)

export default FixedContainer
