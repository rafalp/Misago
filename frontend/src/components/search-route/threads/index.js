import React from "react"
import SearchPage from "../page"
import Results from "./results"

export default function (props) {
  return (
    <SearchPage provider={props.route.provider} search={props.search}>
      <Blankslate
        loading={props.search.isLoading}
        query={props.search.query}
        posts={props.posts}
      >
        <Results
          provider={props.route.provider}
          query={props.search.query}
          {...props.posts}
        />
      </Blankslate>
    </SearchPage>
  )
}

export function Blankslate({ children, loading, posts, query }) {
  if (posts && posts.count) return children

  if (query.length) {
    return (
      <p className="lead">
        {loading
          ? pgettext("search threads", "Loading results...")
          : pgettext(
              "search threads",
              "No threads matching search query have been found."
            )}
      </p>
    )
  }

  return (
    <p className="lead">
      {pgettext(
        "search threads",
        "Enter at least two characters to search threads."
      )}
    </p>
  )
}
