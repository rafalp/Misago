import React from "react"

export default function (props) {
  return (
    <div className="poll-choices-bars">
      {props.poll.choices.map((choice) => {
        return (
          <PollChoice choice={choice} key={choice.hash} poll={props.poll} />
        )
      })}
    </div>
  )
}

export function PollChoice(props) {
  let proc = 0
  if (props.choice.votes && props.poll.votes) {
    proc = Math.ceil((props.choice.votes * 100) / props.poll.votes)
  }

  return (
    <dl className="dl-horizontal">
      <dt>{props.choice.label}</dt>
      <dd>
        <div className="progress">
          <div
            className="progress-bar"
            role="progressbar"
            aria-valuenow={proc}
            aria-valuemin="0"
            aria-valuemax="100"
            style={{ width: proc + "%" }}
          >
            <span className="sr-only">
              {getVotesLabel(props.votes, props.proc)}
            </span>
          </div>
        </div>
        <ul className="list-unstyled list-inline poll-chart">
          <ChoiceVotes proc={proc} votes={props.choice.votes} />
          <UserChoice selected={props.choice.selected} />
        </ul>
      </dd>
    </dl>
  )
}

export function ChoiceVotes(props) {
  return (
    <li className="poll-chart-votes">
      {getVotesLabel(props.votes, props.proc)}
    </li>
  )
}

export function getVotesLabel(votes, proc) {
  const message = npgettext(
    "thread poll",
    "%(votes)s vote, %(proc)s% of total.",
    "%(votes)s votes, %(proc)s% of total.",
    votes
  )

  return interpolate(
    message,
    {
      votes: votes,
      proc: proc,
    },
    true
  )
}

export function UserChoice(props) {
  if (!props.selected) return null

  return (
    <li className="poll-chart-selected">
      <span className="material-icon">check_box</span>
      {pgettext("thread poll", "You've voted on this choice.")}
    </li>
  )
}
