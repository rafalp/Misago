import React from "react"
import { ListGroupEmpty } from "../ListGroup"
import SearchResultsList from "./SearchResultsList"

export default function SearchResultsEmpty() {
  return (
    <SearchResultsList>
      <ListGroupEmpty
        message={pgettext("search results", "Search returned no results.")}
      />
    </SearchResultsList>
  )
}
