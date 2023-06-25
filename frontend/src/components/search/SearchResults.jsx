import React from "react"
import { ListGroupItem } from "../ListGroup"
import SearchResultsList from "./SearchResultsList"
import SearchResultPost from "./SearchResultPost"
import SearchResultUser from "./SearchResultUser"

export default function SearchResults({ query, results }) {
  const threads = results[0]
  const users = results[1]

  const { count } = threads.results

  return (
    <SearchResultsList>
      {users.results.results.map((user) => (
        <SearchResultUser key={user.id} user={user} />
      ))}
      {threads.results.results.map((post) => (
        <SearchResultPost key={post.id} post={post} />
      ))}
      {count > 0 && (
        <ListGroupItem>
          <a
            href={threads.url + "?q=" + encodeURIComponent(query)}
            className="btn btn-default btn-block"
          >
            {npgettext(
              "search results list",
              "See all %(count)s result.",
              "See all %(count)s results.",
              threads.results.count
            ).replace("%(count)s", threads.results.count)}
          </a>
        </ListGroupItem>
      )}
    </SearchResultsList>
  )
}
