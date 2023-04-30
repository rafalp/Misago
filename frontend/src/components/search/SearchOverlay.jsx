import React from "react"
import { connect } from "react-redux"
import { Overlay, OverlayHeader } from "../Overlay"
import SearchFetch from "./SearchFetch"
import SearchInput from "./SearchInput"
import SearchQuery from "./SearchQuery"

function SearchOverlay({ open }) {
  return (
    <Overlay
      open={open}
      onOpen={() => {
        window.setTimeout(() => {
          document.querySelector("#search-mount .form-control-search").focus()
        }, 0)
      }}
    >
      <OverlayHeader>{pgettext("cta", "Search")}</OverlayHeader>
      <SearchQuery>
        {({ query, setQuery }) => {
          return (
            <div className="search-overlay-body">
              <SearchInput query={query} setQuery={setQuery} />
              <div className="search-results-container">
                <SearchFetch query={query} />
              </div>
            </div>
          )
        }}
      </SearchQuery>
    </Overlay>
  )
}

function select(state) {
  return { open: state.overlay.search }
}

const SearchOverlayConnected = connect(select)(SearchOverlay)

export default SearchOverlayConnected
