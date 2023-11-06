import React from "react"

const RankUsersLeft = ({ users }) => {
  if (users.more) {
    return (
      <p>
        {interpolate(
          npgettext(
            "rank users list",
            "There is %(more)s more user with this rank.",
            "There are %(more)s more users with this rank.",
            users.more
          ),
          { more: users.more },
          true
        )}
      </p>
    )
  }

  return (
    <p>
      {pgettext(
        "rank users list empty",
        "There are no more users with this rank."
      )}
    </p>
  )
}

export default RankUsersLeft
