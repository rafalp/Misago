import React from "react"
import SearchFetch from "./SearchFetch"
import SearchInput from "./SearchInput"
import SearchQuery from "./SearchQuery"

export default function SearchDropdown() {
  return (
    <SearchQuery>
      {({ query, setQuery }) => {
        return (
          <div className="search-dropdown-body">
            <SearchInput query={query} setQuery={setQuery} />
            <SearchFetch query={query} />
          </div>
        )
      }}
    </SearchQuery>
  )
}
