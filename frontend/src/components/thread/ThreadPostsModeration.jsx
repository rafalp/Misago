import React from "react"

const ThreadPostsModeration = ({ disabled, dropup }) => (
  <div className={dropup ? "dropup" : "dropdown"}>
    <button
      type="button"
      className="btn btn-default btn-outline btn-icon dropdown-toggle"
      title={gettext("Posts options")}
      data-toggle="dropdown"
      aria-haspopup="true"
      aria-expanded="false"
      disabled={disabled}
    >
      <span className="material-icon">settings</span>
    </button>
    <ul className="dropdown-menu dropdown-menu-right stick-to-bottom">
      <li>HER</li>
    </ul>
  </div>
)

export default ThreadPostsModeration