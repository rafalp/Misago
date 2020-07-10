import classnames from "classnames"
import React from "react"

interface IFixedContainerProps {
  children: React.ReactNode
  className?: string
  show?: boolean
}

const FixedContainer: React.FC<IFixedContainerProps> = ({
  children,
  className,
  show,
}) => (
  <div className={classnames("fixed-container", { show: show }, className)}>
    <div className="container-fluid">{children}</div>
  </div>
)

export default FixedContainer
