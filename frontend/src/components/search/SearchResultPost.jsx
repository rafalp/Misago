import React from "react"
import { ListGroupItem } from "../ListGroup"
import Timestamp from "../Timestamp"

export default function SearchResultPost({ post }) {
  return (
    <ListGroupItem className="search-result">
      <a href={post.url.index}>
        <div className="search-result-card">
          <div className="search-result-name">{post.thread.title}</div>
          <div
            className="search-result-summary"
            dangerouslySetInnerHTML={{ __html: post.headline || post.content }}
          />
          <ul className="search-result-details">
            <li>
              <b>{post.category.name}</b>
            </li>
            <li>{post.poster ? post.poster.username : post.poster_name}</li>
            <li>
              <Timestamp datetime={post.posted_on} />
            </li>
          </ul>
        </div>
      </a>
    </ListGroupItem>
  )
}
