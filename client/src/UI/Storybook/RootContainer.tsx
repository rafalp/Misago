import classnames from "classnames"
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
    className={classnames({
      "d-flex justify-content-center": center,
      "px-3 py-4": padding,
    })}
  >
    {children}
  </div>
)

export default RootContainer
