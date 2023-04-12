import React from "react"

export default function NotificationsList({ items, hasNext, hasPrevious }) {
  return (
    <div className="notifications-list">
      <ul className="list-group">
        {items.map((notification) => (
          <li
            key={notification.id}
            className="list-group-item notifications-list-itemm"
          >
            <div dangerouslySetInnerHTML={{__html: notification.message}} />
          </li>
        ))}
      </ul>
    </div>
  )
}
