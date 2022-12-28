import classnames from "classnames"
import React from "react"

const ToolbarSection = ({ auto, children, className }) => (
  <div
    className={classnames(
      "toolbar-section",
      { "toolbar-section-auto": auto },
      className
    )}
  >
    {children}
  </div>
)

export default ToolbarSection
