import classnames from "classnames"
import React from "react"
import ListGroupItem from "./ListGroupItem"

export default function ListGroupLoading({ className, message }) {
  return (
    <ListGroupItem className={classnames("list-group-loading", className)}>
      <p className="list-group-loading-message">{message}</p>
      <div className="list-group-loading-progress">
        <div className="list-group-loading-progress-bar"></div>
      </div>
    </ListGroupItem>
  )
}
