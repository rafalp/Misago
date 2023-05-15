import classnames from "classnames"
import React from "react"
import ListGroupItem from "./ListGroupItem"

export default function ListGroupError({ className, icon, message, detail }) {
  return (
    <ListGroupItem className={classnames("list-group-error", className)}>
      {!!icon && (
        <div className="list-group-error-icon">
          <span className="material-icon">{icon}</span>
        </div>
      )}
      <p className="list-group-error-message">{message}</p>
      {!!detail && <p className="list-group-error-detail">{detail}</p>}
    </ListGroupItem>
  )
}
