import React from "react"

const ThreadsListEmpty = ({ category, list, message }) => {
  if (list.type === "all") {
    if (message) {
      return (
        <li className="list-group-item empty-message">
          <p className="lead">{message}</p>
          <p>{gettext("Why not start one yourself?")}</p>
        </li>
      )
    }

    return (
      <li className="list-group-item empty-message">
        <p className="lead">
          {category.special_role
            ? gettext("There are no threads on this forum... yet!")
            : gettext("There are no threads in this category.")}
        </p>
        <p>{gettext("Why not start one yourself?")}</p>
      </li>
    )
  }

  return (
    <li className="list-group-item empty-message">
      <p className="lead">
        {gettext("No threads matching specified criteria were found.")}
      </p>
    </li>
  )
}

export default ThreadsListEmpty
