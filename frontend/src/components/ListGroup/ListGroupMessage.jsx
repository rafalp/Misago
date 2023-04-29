import classnames from "classnames"
import React from "react"
import ListGroupItem from "./ListGroupItem"

export default function ListGroupMessage({ className, icon, message, detail }) {
  return (
    <ListGroupItem className={classnames("list-group-message", className)}>
      {!!icon && (
        <div className="list-group-message-icon">
          <span className="material-icon">{icon}</span>
        </div>
      )}
      <p className="list-group-message-message">{message}</p>
      {!!detail && <p className="list-group-message-detail">{detail}</p>}
    </ListGroupItem>
  )
}
