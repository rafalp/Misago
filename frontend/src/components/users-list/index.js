import React from "react"
import Card from "./card"
import Preview from "./preview"

export default function ({ cols, isReady, showStatus, users }) {
  let colClassName = "col-xs-12 col-sm-4"
  if (cols === 4) {
    colClassName += " col-md-3"
  }

  if (!isReady) {
    return <Preview colClassName={colClassName} cols={cols} />
  }

  return (
    <div className="users-cards-list ui-ready">
      <div className="row">
        {users.map((user) => {
          return (
            <div className={colClassName} key={user.id}>
              <Card showStatus={showStatus} user={user} />
            </div>
          )
        })}
      </div>
    </div>
  )
}
