import React from "react"
import UserStatus, { StatusLabel } from "misago/components/user-status"
import hasVisibleTitle from "./has-visible-title"

export default function ({ poster }) {
  let className = "hidden-xs"
  if (hasVisibleTitle(poster)) {
    className += " hidden-sm"
  }

  return (
    <span className={className}>
      <UserStatus status={poster.status}>
        <StatusLabel status={poster.status} user={poster} />
      </UserStatus>
    </span>
  )
}
