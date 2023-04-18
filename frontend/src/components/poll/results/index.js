import React from "react"
import Chart from "./chart"
import Options from "./options"
import PollInfo from "../info"

export default function (props) {
  return (
    <div className="panel panel-default panel-poll">
      <div className="panel-body">
        <h2>{props.poll.question}</h2>
        <PollInfo poll={props.poll} />
        <Chart poll={props.poll} />
        <Options
          isPollOver={props.isPollOver}
          poll={props.poll}
          edit={props.edit}
          showVoting={props.showVoting}
          thread={props.thread}
        />
      </div>
    </div>
  )
}
