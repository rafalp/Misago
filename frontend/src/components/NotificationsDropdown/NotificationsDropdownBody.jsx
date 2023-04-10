import classnames from "classnames"
import React from "react"

export default function NotificationsDropdownBody({
  children,
  showUnread,
  showRead,
  unread,
}) {
  return (
    <div className="notifications-dropdown-body">
      <div>
        <Button active={unread} onClick={showUnread}>
          {pgettext("notifications dropdown", "Unread")}
        </Button>
        <Button active={!unread} onClick={showRead}>
          {pgettext("notifications dropdown", "Read")}
        </Button>
      </div>
      {children}
    </div>
  )
}

function Button({ active, children, onClick }) {
  return (
    <button
      className={classnames("btn", {
        "btn-primary": active,
        "btn-default": !active,
      })}
      type="button"
      onClick={onClick}
    >
      {children}
    </button>
  )
}
