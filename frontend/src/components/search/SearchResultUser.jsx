import React from "react"
import Avatar from "../avatar"
import { ListGroupItem } from "../ListGroup"
import Timestamp from "../Timestamp"

export default function SearchResultUser({ user }) {
  const title = user.title || user.rank.title

  return (
    <ListGroupItem className="search-result">
      <a href={user.url}>
        <Avatar user={user} size={32} />
        <div className="search-result-card">
          <div className="search-result-name">{user.username}</div>
          <ul className="search-result-details">
            {!!title && (
              <li>
                <b>{title}</b>
              </li>
            )}
            <li>{user.rank.name}</li>
            <li>
              <Timestamp datetime={user.joined_on} />
            </li>
          </ul>
        </div>
      </a>
    </ListGroupItem>
  )
}
