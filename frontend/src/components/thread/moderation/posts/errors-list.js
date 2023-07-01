import React from "react"

export default function ({ errors, posts }) {
  return (
    <div className="modal-dialog" role="document">
      <div className="modal-content">
        <div className="modal-header">
          <button
            aria-label={pgettext("modal", "Close")}
            className="close"
            data-dismiss="modal"
            type="button"
          >
            <span aria-hidden="true">&times;</span>
          </button>
          <h4 className="modal-title">
            {pgettext("thread posts moderation modal title", "Moderation")}
          </h4>
        </div>
        <div className="modal-body">
          <p className="lead">
            {pgettext(
              "thread posts moderation modal",
              "One or more posts could not be changed:"
            )}
          </p>

          <ul className="list-unstyled list-errored-items">
            {errors.map((post) => {
              return (
                <PostErrors
                  errors={post.detail}
                  key={post.id}
                  post={posts[post.id]}
                />
              )
            })}
          </ul>
        </div>
      </div>
    </div>
  )
}

export function PostErrors({ errors, post }) {
  const heading = interpolate(
    pgettext("thread posts moderation modal", "%(username)s on %(posted_on)s"),
    {
      posted_on: post.posted_on.format("LL, LT"),
      username: post.poster_name,
    },
    true
  )

  return (
    <li>
      <h5>{heading}:</h5>
      {errors.map((error, i) => {
        return <p key={i}>{error}</p>
      })}
    </li>
  )
}
