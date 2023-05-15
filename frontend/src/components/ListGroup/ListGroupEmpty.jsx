import classnames from "classnames"
import React from "react"
import ListGroupItem from "./ListGroupItem"

export default function ListGroupEmpty({ className, icon, message }) {
  return (
    <ListGroupItem className={classnames("list-group-empty", className)}>
      {!!icon && (
        <div className="list-group-empty-icon">
          <span className="material-icon">{icon}</span>
        </div>
      )}
      <p className="list-group-empty-message">{message}</p>
    </ListGroupItem>
  )
}
