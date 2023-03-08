import React from "react"
import escapeHtml from "misago/utils/escape-html"

const DATE_ABBR = '<abbr title="%(absolute)s">%(relative)s</abbr>'
const USER_SPAN = '<span class="item-title">%(user)s</span>'
const USER_URL = '<a href="%(url)s" class="item-title">%(user)s</a>'

export default function (props) {
  return (
    <ul className="list-unstyled list-inline poll-help">
      <PollChoicesLeft choicesLeft={props.choicesLeft} />
      <PollAllowRevote poll={props.poll} />
    </ul>
  )
}

export function PollChoicesLeft({ choicesLeft }) {
  if (choicesLeft === 0) {
    return (
      <li className="poll-help-choices-left">
        {pgettext("thread poll", "You can't select any more choices.")}
      </li>
    )
  }

  const message = npgettext(
    "thread poll",
    "You can select %(choices)s more choice.",
    "You can select %(choices)s more choices.",
    choicesLeft
  )

  const label = interpolate(
    message,
    {
      choices: choicesLeft,
    },
    true
  )

  return <li className="poll-help-choices-left">{label}</li>
}

export function PollAllowRevote(props) {
  if (props.poll.allow_revotes) {
    return (
      <li className="poll-help-allow-revotes">
        {pgettext("thread poll", "You can change your vote later.")}
      </li>
    )
  }

  return (
    <li className="poll-help-no-revotes">
      {pgettext("thread poll", "Votes are final.")}
    </li>
  )
}
