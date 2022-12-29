import React from "react"
import Avatar from "misago/components/avatar"
import Stats from "./stats"
import UserTitle from "./user-title"

export default function ({ showStatus, user }) {
  const { rank } = user

  let className = "panel user-card"
  if (rank.css_class) {
    className += " user-card-" + rank.css_class
  }

  return (
    <div className={className}>
      <div className="panel-body">
        <div className="row">
          <div className="col-xs-3 user-card-left">
            <div className="user-card-small-avatar">
              <a href={user.url}>
                <Avatar size="50" size2x="80" user={user} />
              </a>
            </div>
          </div>
          <div className="col-xs-9 col-sm-12 user-card-body">
            <div className="user-card-avatar">
              <a href={user.url}>
                <Avatar size="150" size2x="200" user={user} />
              </a>
            </div>

            <div className="user-card-username">
              <a href={user.url}>{user.username}</a>
            </div>
            <div className="user-card-title">
              <UserTitle rank={rank} title={user.title} />
            </div>

            <div className="user-card-stats">
              <Stats showStatus={showStatus} user={user} />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
