import classNames from "classnames"
import React from "react"

interface IMobileOnly {
  children: React.ReactNode
  noSpace?: boolean
}

const MobileOnly: React.FC<IMobileOnly> = ({ children, noSpace }) => (
  <div className={classNames("d-md-none", { "mb-3": noSpace })}>
    {children}
  </div>
)

export default MobileOnly
