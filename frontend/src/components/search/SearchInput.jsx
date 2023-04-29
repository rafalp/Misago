import React from "react"

export default function SearchInput({ query, setQuery }) {
  return (
    <div className="search-input">
      <input
        className="form-control form-control-search"
        type="text"
        placeholder={pgettext("cta", "Search")}
        value={query}
        onChange={(event) => setQuery(event.target.value)}
      />
    </div>
  )
}
