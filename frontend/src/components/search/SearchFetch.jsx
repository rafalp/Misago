import React from "react"
import { ApiFetch } from "../Api"
import SearchMessage from "./SearchMessage"
import SearchResults from "./SearchResults"
import SearchResultsEmpty from "./SearchResultsEmpty"
import SearchResultsError from "./SearchResultsError"
import SearchResultsLoading from "./SearchResultsLoading"

const DEBOUNCE = 750
const CACHE = {}

export default class SearchFetch extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      query: this.props.query.trim(),
    }

    this.debounce = null
  }

  componentDidUpdate() {
    const query = this.props.query.trim()

    if (this.state.query != query) {
      if (this.debounce) {
        window.clearTimeout(this.debounce)
      }

      this.debounce = window.setTimeout(() => {
        this.setState({ query })
      }, DEBOUNCE)
    }
  }

  componentWillUnmount() {
    if (this.debounce) {
      window.clearTimeout(this.debounce)
    }
  }

  render() {
    return (
      <ApiFetch
        url={getSearchUrl(this.state.query)}
        cache={CACHE}
        disabled={this.state.query.length < 3}
      >
        {({ data, loading, error }) => {
          if (this.state.query.length < 3) {
            return <SearchMessage />
          }

          if (loading) {
            return <SearchResultsLoading />
          }

          if (error) {
            return <SearchResultsError error={error} />
          }

          if (isResultEmpty(data)) {
            return <SearchResultsEmpty />
          }

          if (data !== null) {
            return <SearchResults query={this.state.query} results={data} />
          }

          return null
        }}
      </ApiFetch>
    )
  }
}

function getSearchUrl(query) {
  return misago.get("SEARCH_API") + "?q=" + encodeURIComponent(query)
}

function isResultEmpty(results) {
  if (results === null) {
    return true
  }

  let resultsCount = 0
  results.forEach((result) => {
    resultsCount += result.results.count
  })
  return resultsCount === 0
}
