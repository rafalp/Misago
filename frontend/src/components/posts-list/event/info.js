import React from "react"
import escapeHtml from "misago/utils/escape-html"
import Controls from "./controls"

const DATE_ABBR = '<abbr title="%(absolute)s">%(relative)s</abbr>'
const DATE_URL = '<a href="%(url)s" title="%(absolute)s">%(relative)s</a>'
const USER_SPAN = '<span class="item-title">%(user)s</span>'
const USER_URL = '<a href="%(url)s" class="item-title">%(user)s</a>'

export default function (props) {
  return (
    <ul className="list-inline event-info">
      <Hidden {...props} />
      <Poster {...props} />
      <Controls {...props} />
    </ul>
  )
}

export function Hidden(props) {
  if (props.post.is_hidden) {
    let user = null
    if (props.post.url.hidden_by) {
      user = interpolate(
        USER_URL,
        {
          url: escapeHtml(props.post.url.hidden_by),
          user: escapeHtml(props.post.hidden_by_name),
        },
        true
      )
    } else {
      user = interpolate(
        USER_SPAN,
        {
          user: escapeHtml(props.post.hidden_by_name),
        },
        true
      )
    }

    const date = interpolate(
      DATE_ABBR,
      {
        absolute: escapeHtml(props.post.hidden_on.format("LLL")),
        relative: escapeHtml(props.post.hidden_on.fromNow()),
      },
      true
    )

    const message = interpolate(
      escapeHtml(
        pgettext("event info", "Hidden by %(event_by)s %(event_on)s.")
      ),
      {
        event_by: user,
        event_on: date,
      },
      true
    )

    return (
      <li
        className="event-hidden-message"
        dangerouslySetInnerHTML={{ __html: message }}
      />
    )
  } else {
    return null
  }
}

export function Poster(props) {
  let user = null
  if (props.post.poster) {
    user = interpolate(
      USER_URL,
      {
        url: escapeHtml(props.post.poster.url),
        user: escapeHtml(props.post.poster_name),
      },
      true
    )
  } else {
    user = interpolate(
      USER_SPAN,
      {
        user: escapeHtml(props.post.poster_name),
      },
      true
    )
  }

  const date = interpolate(
    DATE_URL,
    {
      url: escapeHtml(props.post.url.index),
      absolute: escapeHtml(props.post.posted_on.format("LLL")),
      relative: escapeHtml(props.post.posted_on.fromNow()),
    },
    true
  )

  const message = interpolate(
    escapeHtml(pgettext("event info", "By %(event_by)s %(event_on)s.")),
    {
      event_by: user,
      event_on: date,
    },
    true
  )

  return (
    <li
      className="event-posters"
      dangerouslySetInnerHTML={{ __html: message }}
    />
  )
}
