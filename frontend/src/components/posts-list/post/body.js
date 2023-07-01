import React from "react"
import Waypoint from "../waypoint"
import MisagoMarkup from "misago/components/misago-markup"
import escapeHtml from "misago/utils/escape-html"

const HIDDEN_BY_URL = '<a href="%(url)s" class="item-title">%(user)s</a>'
const HIDDEN_BY_SPAN = '<span class="item-title">%(user)s</span>'
const HIDDEN_ON =
  '<abbr class="last-title" title="%(absolute)s">%(relative)s</abbr>'

export default function (props) {
  if (props.post.is_hidden && !props.post.acl.can_see_hidden) {
    return <Hidden {...props} />
  } else if (props.post.content) {
    return <Default {...props} />
  } else {
    return <Invalid {...props} />
  }
}

export function Default({ post }) {
  const poster = "@" + (post.poster ? post.poster.username : post.poster_name)

  return (
    <Waypoint className="post-body" post={post}>
      <MisagoMarkup author={poster} markup={post.content} />
    </Waypoint>
  )
}

export function Hidden(props) {
  let user = null
  if (props.post.hidden_by) {
    user = interpolate(
      HIDDEN_BY_URL,
      {
        url: escapeHtml(props.post.url.hidden_by),
        user: escapeHtml(props.post.hidden_by_name),
      },
      true
    )
  } else {
    user = interpolate(
      HIDDEN_BY_SPAN,
      {
        user: escapeHtml(props.post.hidden_by_name),
      },
      true
    )
  }

  const date = interpolate(
    HIDDEN_ON,
    {
      absolute: escapeHtml(props.post.hidden_on.format("LLL")),
      relative: escapeHtml(props.post.hidden_on.fromNow()),
    },
    true
  )

  const message = interpolate(
    escapeHtml(
      pgettext("post body hidden", "Hidden by %(hidden_by)s %(hidden_on)s.")
    ),
    {
      hidden_by: user,
      hidden_on: date,
    },
    true
  )

  return (
    <Waypoint className="post-body post-body-hidden" post={props.post}>
      <p className="lead">
        {pgettext(
          "post body hidden",
          "This post is hidden. You cannot see its contents."
        )}
      </p>
      <p className="text-muted" dangerouslySetInnerHTML={{ __html: message }} />
    </Waypoint>
  )
}

export function Invalid(props) {
  return (
    <Waypoint className="post-body post-body-invalid" post={props.post}>
      <p className="lead">
        {pgettext(
          "post body invalid",
          "This post's contents cannot be displayed."
        )}
      </p>
      <p className="text-muted">
        {pgettext(
          "post body invalid",
          "This error is caused by invalid post content manipulation."
        )}
      </p>
    </Waypoint>
  )
}
