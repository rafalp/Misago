import React from "react"
import Dropdown from "./dropdown"

export default function (props) {
  return (
    <div className="pull-right dropdown">
      <button
        aria-expanded="true"
        aria-haspopup="true"
        className="btn btn-default btn-icon dropdown-toggle"
        data-toggle="dropdown"
        type="button"
      >
        <span className="material-icon">expand_more</span>
      </button>
      <Dropdown {...props} />
    </div>
  )
}
