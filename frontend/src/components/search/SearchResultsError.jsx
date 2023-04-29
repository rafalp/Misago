import React from "react"
import { ListGroupError } from "../ListGroup"
import SearchResultsList from "./SearchResultsList"

export default function SearchResultsError({ error }) {
  return (
    <SearchResultsList>
      <ListGroupError
        message={pgettext(
          "search results",
          "Search results could not be loaded."
        )}
        detail={errorDetail(error)}
      />
    </SearchResultsList>
  )
}

function errorDetail(error) {
  if (error.status === 0) {
    return gettext(
      "Check your internet connection and try refreshing the site."
    )
  }

  if (error.data && error.data.detail) {
    return error.data.detail
  }
}
