import React from "react"
import Card from "./card"

export default function ({ participants, thread, user, userIsOwner }) {
  return (
    <div className="participants-cards">
      <div className="row">
        {participants.map((participant) => {
          return (
            <Card
              key={participant.id}
              participant={participant}
              thread={thread}
              user={user}
              userIsOwner={userIsOwner}
            />
          )
        })}
      </div>
    </div>
  )
}
