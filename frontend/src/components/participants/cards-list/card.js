import React from "react"
import MakeOwner from "./make-owner"
import Remove from "./remove"
import Avatar from "misago/components/avatar"

export default function (props) {
  const participant = props.participant

  let className = "btn btn-default"
  if (participant.is_owner) {
    className = "btn btn-primary"
  }
  className += " btn-user btn-block"

  return (
    <div className="col-xs-12 col-sm-3 col-md-2 participant-card">
      <div className="dropdown">
        <button
          aria-haspopup="true"
          aria-expanded="false"
          className={className}
          data-toggle="dropdown"
          type="button"
        >
          <Avatar size="34" user={participant} />
          <span className="btn-text">{participant.username}</span>
        </button>
        <ul className="dropdown-menu stick-to-bottom">
          <UserStatus isOwner={participant.is_owner} />
          <li className="dropdown-header" />
          <li>
            <a href={participant.url}>
              {pgettext("thread participants profile link", "See profile")}
            </a>
          </li>
          <li role="separator" className="divider" />
          <MakeOwner {...props} />
          <Remove {...props} />
        </ul>
      </div>
    </div>
  )
}

export function UserStatus({ isOwner }) {
  if (!isOwner) return null

  return (
    <li className="dropdown-header dropdown-header-owner">
      <span className="material-icon">start</span>
      <span className="icon-text">
        {pgettext("thread participants owner status", "Thread owner")}
      </span>
    </li>
  )
}
