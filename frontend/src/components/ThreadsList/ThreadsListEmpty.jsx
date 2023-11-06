import React from "react"

const ThreadsListEmpty = ({ category, list, message }) => {
  if (list.type === "all") {
    if (message) {
      return (
        <li className="list-group-item empty-message">
          <p className="lead">{message}</p>
        </li>
      )
    }

    return (
      <li className="list-group-item empty-message">
        <p className="lead">
          {category.special_role
            ? pgettext(
                "threads list empty",
                "There are no threads on this site yet."
              )
            : pgettext(
                "threads list empty",
                "There are no threads in this category."
              )}
        </p>
      </li>
    )
  }

  return (
    <li className="list-group-item empty-message">
      <p className="lead">
        {pgettext(
          "threads list empty",
          "No threads matching specified criteria were found."
        )}
      </p>
    </li>
  )
}

export default ThreadsListEmpty
