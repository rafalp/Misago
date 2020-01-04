import classNames from "classnames"
import React from "react"

interface IRootContainerProps {
  children: React.ReactNode
  padding?: boolean
}

const RootContainer: React.FC<IRootContainerProps> = ({ children, padding }) => (
  <div className={classNames({"p-4": padding})}>
    {children}
  </div>
)

export default RootContainer
