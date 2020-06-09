import React from "react"

const ButtonSpinner: React.FC = () => (
  <span className="btn-spinner">
    <span
      className="spinner-border spinner-border-sm"
      role="status"
      aria-hidden="true"
    />
  </span>
)

export default ButtonSpinner
