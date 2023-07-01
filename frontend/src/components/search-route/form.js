import React from "react"
import misago from "misago"
import Form from "misago/components/form"
import { load as updatePosts } from "misago/reducers/posts"
import { update as updateSearch } from "misago/reducers/search"
import { hydrate as updateUsers } from "misago/reducers/users"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"
import { FlexRow, FlexRowCol, FlexRowSection } from "../FlexRow"
import {
  PageHeader,
  PageHeaderContainer,
  PageHeaderBanner,
  PageHeaderDetails,
} from "../PageHeader"

export default class extends Form {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false,
      query: props.search.query,
    }
  }

  componentDidMount() {
    if (this.state.query.length) {
      this.handleSubmit()
    }
  }

  onQueryChange = (event) => {
    this.changeValue("query", event.target.value)
  }

  clean() {
    if (!this.state.query.trim().length) {
      snackbar.error(pgettext("search form", "You have to enter search query."))
      return false
    }

    return true
  }

  send() {
    store.dispatch(
      updateSearch({
        isLoading: true,
      })
    )

    const query = this.state.query.trim()

    let url = window.location.href
    const urlQuery = url.indexOf("?q=")
    if (urlQuery > 0) {
      url = url.substring(0, urlQuery + 3)
    }
    window.history.pushState({}, "", url + encodeURIComponent(query))

    return ajax.get(misago.get("SEARCH_API"), { q: query })
  }

  handleSuccess(providers) {
    store.dispatch(
      updateSearch({
        query: this.state.query.trim(),
        isLoading: false,
        providers,
      })
    )

    providers.forEach((provider) => {
      if (provider.id === "users") {
        store.dispatch(updateUsers(provider.results.results))
      } else if (provider.id === "threads") {
        store.dispatch(updatePosts(provider.results))
      }
    })
  }

  handleError(rejection) {
    snackbar.apiError(rejection)

    store.dispatch(
      updateSearch({
        isLoading: false,
      })
    )
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <PageHeaderContainer>
          <PageHeader styleName="site-search">
            <PageHeaderBanner styleName="site-search">
              <h1>{pgettext("search form title", "Search")}</h1>
            </PageHeaderBanner>
            <PageHeaderDetails className="page-header-search-form">
              <FlexRow>
                <FlexRowSection auto>
                  <FlexRowCol>
                    <input
                      className="form-control"
                      disabled={this.state.isLoading}
                      type="text"
                      value={this.state.query}
                      placeholder={pgettext("search form input", "Search")}
                      onChange={this.onQueryChange}
                    />
                  </FlexRowCol>
                  <FlexRowCol shrink>
                    <button
                      className="btn btn-secondary btn-icon btn-outline"
                      title={pgettext("search form btn", "Search")}
                      disabled={this.state.isLoading}
                    >
                      <span className="material-icon">search</span>
                    </button>
                  </FlexRowCol>
                </FlexRowSection>
              </FlexRow>
            </PageHeaderDetails>
          </PageHeader>
        </PageHeaderContainer>
      </form>
    )
  }
}
