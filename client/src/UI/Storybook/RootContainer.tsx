import classNames from "classnames"
import React from "react"

interface IRootContainerProps {
  children: React.ReactNode
  center?: boolean
  padding?: boolean
}

const RootContainer: React.FC<IRootContainerProps> = ({
  children,
  center,
  padding,
}) => (
  <div
    className={classNames({
      "d-flex justify-content-center": center,
      "p-4": padding,
    })}
  >
    {children}
  </div>
)

export default RootContainer
