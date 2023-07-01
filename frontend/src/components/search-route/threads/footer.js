import React from "react"
import MisagoMarkup from "misago/components/misago-markup"
import escapeHtml from "misago/utils/escape-html"

const CATEGORY_SPAN = '<span class="category-name">%(name)s</span>'
const ITEM_SPAN = '<span class="item-title">%(name)s</span>'

export default function (props) {
  const template = pgettext(
    "search threads result",
    '%(user)s, %(posted_on)s in "%(thread)s", %(category)s'
  )

  let username = null
  if (props.post.poster) {
    username = props.post.poster.username
  } else {
    username = props.post.poster_name
  }

  const message = interpolate(
    escapeHtml(template),
    {
      category: interpolate(
        CATEGORY_SPAN,
        {
          name: escapeHtml(props.category.name),
        },
        true
      ),
      thread: interpolate(
        ITEM_SPAN,
        {
          name: escapeHtml(props.thread.title),
        },
        true
      ),
      user: interpolate(
        ITEM_SPAN,
        {
          name: escapeHtml(username),
        },
        true
      ),
      posted_on: escapeHtml(props.post.hidden_on.fromNow()),
    },
    true
  )

  return (
    <div className="panel-footer post-infeed-footer">
      <a
        dangerouslySetInnerHTML={{ __html: message }}
        href={props.post.url.index}
      />
    </div>
  )
}
