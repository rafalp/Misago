import React from "react"
import Avatar from "./avatar"

const ThreadStarterCard = ({ thread }) => (
  <div className="thread-user-card">
    <div className="thread-user-card-media">
      {thread.starter ? (
        <a href={thread.url.starter}>
          <Avatar size={40} user={thread.starter} />
        </a>
      ) : (
        <Avatar size={40} />
      )}
    </div>
    <div className="thread-user-card-body">
      <div className="thread-user-card-header">
        {thread.starter ? (
          <a
            className="item-title"
            href={thread.url.starter}
            title={pgettext("thread starter info", "Thread author")}
          >
            {thread.starter.username}
          </a>
        ) : (
          <span
            className="item-title"
            title={pgettext("thread starter info", "Thread author")}
          >
            {thread.starter_name}
          </span>
        )}
      </div>
      <div>
        <span
          className="text-muted"
          title={interpolate(
            pgettext("thread starter info", "Started on: %(timestamp)s"),
            {
              timestamp: thread.started_on.format("LLL"),
            },
            true
          )}
        >
          {thread.started_on.fromNow()}
        </span>
      </div>
    </div>
  </div>
)

export default ThreadStarterCard
