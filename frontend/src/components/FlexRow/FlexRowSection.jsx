import classnames from "classnames"
import React from "react"

const FlexRowSection = ({ auto, children, className }) => (
  <div
    className={classnames(
      "flex-row-section",
      { "flex-row-section-auto": auto },
      className
    )}
  >
    {children}
  </div>
)

export default FlexRowSection
