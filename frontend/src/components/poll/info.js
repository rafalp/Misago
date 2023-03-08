import React from "react"
import escapeHtml from "misago/utils/escape-html"

const DATE_ABBR = '<abbr title="%(absolute)s">%(relative)s</abbr>'
const USER_SPAN = '<span class="item-title">%(user)s</span>'
const USER_URL = '<a href="%(url)s" class="item-title">%(user)s</a>'

export default function (props) {
  return (
    <ul className="list-unstyled list-inline poll-details">
      <PollVotes votes={props.poll.votes} />
      <PollLength poll={props.poll} />
      <PollIsPublic poll={props.poll} />
      <PollCreation poll={props.poll} />
    </ul>
  )
}

export function PollCreation(props) {
  const message = interpolate(
    escapeHtml(pgettext("thread poll", "Started by %(poster)s %(posted_on)s.")),
    {
      poster: getPoster(props.poll),
      posted_on: getPostedOn(props.poll),
    },
    true
  )

  return (
    <li
      className="poll-info-creation"
      dangerouslySetInnerHTML={{ __html: message }}
    />
  )
}

export function getPoster(poll) {
  if (poll.url.poster) {
    return interpolate(
      USER_URL,
      {
        url: escapeHtml(poll.url.poster),
        user: escapeHtml(poll.poster_name),
      },
      true
    )
  }

  return interpolate(
    USER_SPAN,
    {
      user: escapeHtml(poll.poster_name),
    },
    true
  )
}

export function getPostedOn(poll) {
  return interpolate(
    DATE_ABBR,
    {
      absolute: escapeHtml(poll.posted_on.format("LLL")),
      relative: escapeHtml(poll.posted_on.fromNow()),
    },
    true
  )
}

export function PollLength(props) {
  if (!props.poll.length) {
    return null
  }

  const message = interpolate(
    escapeHtml(pgettext("thread poll", "Voting ends %(ends_on)s.")),
    {
      ends_on: getEndsOn(props.poll),
    },
    true
  )

  return (
    <li
      className="poll-info-ends-on"
      dangerouslySetInnerHTML={{ __html: message }}
    />
  )
}

export function getEndsOn(poll) {
  return interpolate(
    DATE_ABBR,
    {
      absolute: escapeHtml(poll.endsOn.format("LLL")),
      relative: escapeHtml(poll.endsOn.fromNow()),
    },
    true
  )
}

export function PollVotes(props) {
  const message = npgettext(
    "thread poll",
    "%(votes)s vote.",
    "%(votes)s votes.",
    props.votes
  )
  const label = interpolate(
    message,
    {
      votes: props.votes,
    },
    true
  )

  return <li className="poll-info-votes">{label}</li>
}

export function PollIsPublic(props) {
  if (!props.poll.is_public) {
    return null
  }

  return (
    <li className="poll-info-public">
      {pgettext("thread poll", "Voting is public.")}
    </li>
  )
}
