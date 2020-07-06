import classnames from "classnames"
import React from "react"

interface IAbsoluteContainerProps {
  children: React.ReactNode
  className?: string
  show?: boolean
}

const AbsoluteContainer: React.FC<IAbsoluteContainerProps> = ({
  children,
  className,
  show,
}) => (
  <div className={classnames("absolute-container", { show: show }, className)}>
    <div className="container-fluid">{children}</div>
  </div>
)

export default AbsoluteContainer
