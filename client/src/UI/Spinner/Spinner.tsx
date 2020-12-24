import classnames from "classnames"
import React from "react"

interface SpinnerProps {
  small?: boolean
}

const Spinner: React.FC<SpinnerProps> = ({ small }) => (
  <div
    className={classnames("spinner-border", { "spinner-border-sm": small })}
    role="status"
  />
)

export default Spinner
