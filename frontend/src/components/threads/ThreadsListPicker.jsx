import React from "react"
import { Link } from "react-router-dom"

const ThreadsListPicker = ({ baseUrl, list, lists }) => (
  <div className="dropdown threads-list-picker">
    <button
      type="button"
      className="btn btn-default btn-outline dropdown-toggle btn-block"
      data-toggle="dropdown"
      aria-haspopup="true"
      aria-expanded="false"
    >
      {list.longName}
    </button>
    <ul className="dropdown-menu stick-to-bottom">
      {lists.map((choice) => (
        <li key={choice.type}>
          <Link to={baseUrl + choice.path}>{choice.longName}</Link>
        </li>
      ))}
    </ul>
  </div>
)

export default ThreadsListPicker
