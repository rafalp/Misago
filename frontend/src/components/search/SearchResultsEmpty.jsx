import React from "react"
import { ListGroupEmpty } from "../ListGroup"
import SearchResultsList from "./SearchResultsList"

export default function SearchResultsEmpty() {
  return (
    <SearchResultsList>
      <ListGroupEmpty
        message={pgettext("search results", "The search returned no results.")}
      />
    </SearchResultsList>
  )
}
