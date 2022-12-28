import React from "react"

const RankUsersLeft = ({ users }) => {
  if (users.more) {
    return (
      <p>{
        interpolate(ngettext(
          "There is %(more)s more member with this role.",
          "There are %(more)s more members with this role.",
          users.more
        ), { more: users.more }, true)
        }</p>
    )
  }

  return <p>{gettext("There are no more members with this role.")}</p>
}

export default RankUsersLeft