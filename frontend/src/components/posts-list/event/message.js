import React from "react"
import escapeHtml from "misago/utils/escape-html"

const MESSAGE = {
  pinned_globally: pgettext(
    "event message",
    "Thread has been pinned globally."
  ),
  pinned_locally: pgettext(
    "event message",
    "Thread has been pinned in category."
  ),
  unpinned: pgettext("event message", "Thread has been unpinned."),

  approved: pgettext("event message", "Thread has been approved."),

  opened: pgettext("event message", "Thread has been opened."),
  closed: pgettext("event message", "Thread has been closed."),

  unhid: pgettext("event message", "Thread has been revealed."),
  hid: pgettext("event message", "Thread has been made hidden."),

  tookover: pgettext("event message", "Took thread over."),

  owner_left: pgettext(
    "event message",
    "Owner has left thread. This thread is now closed."
  ),
  participant_left: pgettext("event message", "Participant has left thread."),
}

const ITEM_LINK = '<a href="%(url)s" class="item-title">%(name)s</a>'
const ITEM_SPAN = '<span class="item-title">%(name)s</span>'

export default function (props) {
  if (MESSAGE[props.post.event_type]) {
    return <p className="event-message">{MESSAGE[props.post.event_type]}</p>
  } else if (props.post.event_type === "changed_title") {
    return <ChangedTitle {...props} />
  } else if (props.post.event_type === "moved") {
    return <Moved {...props} />
  } else if (props.post.event_type === "merged") {
    return <Merged {...props} />
  } else if (props.post.event_type === "changed_owner") {
    return <ChangedOwner {...props} />
  } else if (props.post.event_type === "added_participant") {
    return <AddedParticipant {...props} />
  } else if (props.post.event_type === "removed_participant") {
    return <RemovedParticipant {...props} />
  } else {
    return null
  }
}

export function ChangedTitle(props) {
  const msgstring = escapeHtml(
    pgettext(
      "event message",
      "Thread title has been changed from %(old_title)s."
    )
  )
  const oldTitle = interpolate(
    ITEM_SPAN,
    {
      name: escapeHtml(props.post.event_context.old_title),
    },
    true
  )
  const message = interpolate(
    msgstring,
    {
      old_title: oldTitle,
    },
    true
  )

  return (
    <p
      className="event-message"
      dangerouslySetInnerHTML={{ __html: message }}
    />
  )
}

export function Moved(props) {
  const msgstring = escapeHtml(
    pgettext("event message", "Thread has been moved from %(from_category)s.")
  )
  const fromCategory = interpolate(
    ITEM_LINK,
    {
      url: escapeHtml(props.post.event_context.from_category.url),
      name: escapeHtml(props.post.event_context.from_category.name),
    },
    true
  )

  const message = interpolate(
    msgstring,
    {
      from_category: fromCategory,
    },
    true
  )

  return (
    <p
      className="event-message"
      dangerouslySetInnerHTML={{ __html: message }}
    />
  )
}

export function Merged(props) {
  const msgstring = escapeHtml(
    pgettext(
      "event message",
      "The %(merged_thread)s thread has been merged into this thread."
    )
  )
  const mergedThread = interpolate(
    ITEM_SPAN,
    {
      name: escapeHtml(props.post.event_context.merged_thread),
    },
    true
  )

  const message = interpolate(
    msgstring,
    {
      merged_thread: mergedThread,
    },
    true
  )

  return (
    <p
      className="event-message"
      dangerouslySetInnerHTML={{ __html: message }}
    />
  )
}

export function ChangedOwner(props) {
  const msgstring = escapeHtml(
    pgettext("event message", "Changed thread owner to %(user)s.")
  )
  const newOwner = interpolate(
    ITEM_LINK,
    {
      url: escapeHtml(props.post.event_context.user.url),
      name: escapeHtml(props.post.event_context.user.username),
    },
    true
  )

  const message = interpolate(
    msgstring,
    {
      user: newOwner,
    },
    true
  )

  return (
    <p
      className="event-message"
      dangerouslySetInnerHTML={{ __html: message }}
    />
  )
}

export function AddedParticipant(props) {
  const msgstring = escapeHtml(
    pgettext("event message", "Added %(user)s to thread.")
  )
  const newOwner = interpolate(
    ITEM_LINK,
    {
      url: escapeHtml(props.post.event_context.user.url),
      name: escapeHtml(props.post.event_context.user.username),
    },
    true
  )

  const message = interpolate(
    msgstring,
    {
      user: newOwner,
    },
    true
  )

  return (
    <p
      className="event-message"
      dangerouslySetInnerHTML={{ __html: message }}
    />
  )
}

export function RemovedParticipant(props) {
  const msgstring = escapeHtml(
    pgettext("event message", "Removed %(user)s from thread.")
  )
  const newOwner = interpolate(
    ITEM_LINK,
    {
      url: escapeHtml(props.post.event_context.user.url),
      name: escapeHtml(props.post.event_context.user.username),
    },
    true
  )

  const message = interpolate(
    msgstring,
    {
      user: newOwner,
    },
    true
  )

  return (
    <p
      className="event-message"
      dangerouslySetInnerHTML={{ __html: message }}
    />
  )
}
