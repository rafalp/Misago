import classNames from "classnames"
import React from "react"

interface ISpinnerProps {
  small?: boolean
}

const Spinner: React.FC<ISpinnerProps> = ({ small }) => (
  <div className={classNames("spinner-border", { "spinner-border-sm": small })} role="status" />
)

export default Spinner
