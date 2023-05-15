import React from "react"
import { ListGroupLoading } from "../ListGroup"
import SearchResultsList from "./SearchResultsList"

export default function SearchResultsLoading() {
  return (
    <SearchResultsList>
      <ListGroupLoading message={pgettext("search results", "Searching...")} />
    </SearchResultsList>
  )
}
