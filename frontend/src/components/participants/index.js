import React from "react"
import AddParticipant from "./add-participant"
import CardsList from "./cards-list"
import * as utils from "./utils"

export default function (props) {
  if (!props.participants.length) return null

  return (
    <div className="panel panel-default panel-participants">
      <div className="panel-body">
        <CardsList
          userIsOwner={getUserIsOwner(props.user, props.participants)}
          {...props}
        />
        <div className="row">
          <AddParticipant thread={props.thread} />
          <div className="col-xs-12 col-sm-9">
            <p>{utils.getParticipantsCopy(props.participants)}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export function getUserIsOwner(user, participants) {
  return participants[0].id === user.id
}
