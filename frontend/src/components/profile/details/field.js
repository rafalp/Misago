import React from "react"
import FieldValue from "./field-value"

export default function (props) {
  return (
    <div className="form-group">
      <strong className="control-label col-md-3">{props.name}:</strong>
      <FieldValue {...props} />
    </div>
  )
}
