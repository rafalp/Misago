import React from "react"

export default class SearchQuery extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      query: "",
    }
  }

  setQuery = (query) => {
    this.setState({ query })
  }

  render() {
    return this.props.children({
      query: this.state.query,
      setQuery: this.setQuery,
    })
  }
}
