import React from "react"

export default function ({ isAuthenticated, profile }) {
  let message = null
  if (isAuthenticated) {
    message = pgettext(
      "profile details empty",
      "You are not sharing any details with others."
    )
  } else {
    message = interpolate(
      pgettext(
        "profile details empty",
        "%(username)s is not sharing any details with others."
      ),
      {
        username: profile.username,
      },
      true
    )
  }

  return (
    <div className="panel panel-default">
      <div className="panel-body text-center lead">{message}</div>
    </div>
  )
}
