import classnames from "classnames"
import React from "react"

interface IRootContainerProps {
  children: React.ReactNode
  center?: boolean
  nopadding?: boolean
}

const RootContainer: React.FC<IRootContainerProps> = ({
  children,
  center,
  nopadding,
}) => (
  <div
    className={classnames({
      "d-flex justify-content-center": center,
      "px-3 py-4": !nopadding,
    })}
  >
    {children}
  </div>
)

export default RootContainer
