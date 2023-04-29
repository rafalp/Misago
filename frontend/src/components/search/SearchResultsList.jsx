import React from "react"
import { ListGroup } from "../ListGroup"

export default function SearchResultsList({ children }) {
  return <ListGroup className="search-results-list">{children}</ListGroup>
}
