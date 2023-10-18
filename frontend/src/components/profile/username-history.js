import React from "react"
import Button from "misago/components/button"
import Search from "misago/components/quick-search"
import UsernameHistory from "misago/components/username-history/root"
import misago from "misago/index"
import { hydrate, append } from "misago/reducers/username-history"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"
import title from "misago/services/page-title"
import { Toolbar, ToolbarItem, ToolbarSection } from "../Toolbar"

export default class extends React.Component {
  constructor(props) {
    super(props)

    if (misago.has("PROFILE_NAME_HISTORY")) {
      this.initWithPreloadedData(misago.pop("PROFILE_NAME_HISTORY"))
    } else {
      this.initWithoutPreloadedData()
    }
  }

  initWithPreloadedData(data) {
    this.state = {
      isLoaded: true,
      isBusy: false,

      search: "",

      count: data.count,
      more: data.more,

      page: data.page,
      pages: data.pages,
    }

    store.dispatch(hydrate(data.results))
  }

  initWithoutPreloadedData() {
    this.state = {
      isLoaded: false,
      isBusy: false,

      search: "",

      count: 0,
      more: 0,

      page: 1,
      pages: 1,
    }

    this.loadChanges()
  }

  loadChanges(page = 1, search = null) {
    ajax
      .get(
        misago.get("USERNAME_CHANGES_API"),
        {
          user: this.props.profile.id,
          search: search,
          page: page || 1,
        },
        "search-username-history"
      )
      .then(
        (data) => {
          if (page === 1) {
            store.dispatch(hydrate(data.results))
          } else {
            store.dispatch(append(data.results))
          }

          this.setState({
            isLoaded: true,
            isBusy: false,

            count: data.count,
            more: data.more,

            page: data.page,
            pages: data.pages,
          })
        },
        (rejection) => {
          snackbar.apiError(rejection)
        }
      )
  }

  componentDidMount() {
    title.set({
      title: pgettext("profile username history title", "Username history"),
      parent: this.props.profile.username,
    })
  }

  loadMore = () => {
    this.setState({
      isBusy: true,
    })

    this.loadChanges(this.state.page + 1, this.state.search)
  }

  search = (ev) => {
    this.setState({
      isLoaded: false,
      isBusy: true,

      search: ev.target.value,

      count: 0,
      more: 0,

      page: 1,
      pages: 1,
    })

    this.loadChanges(1, ev.target.value)
  }

  getLabel() {
    if (!this.state.isLoaded) {
      return pgettext("profile username history", "Loading...")
    } else if (this.state.search) {
      let message = npgettext(
        "profile username history",
        "Found %(changes)s username change.",
        "Found %(changes)s username changes.",
        this.state.count
      )

      return interpolate(
        message,
        {
          changes: this.state.count,
        },
        true
      )
    } else if (this.props.profile.id === this.props.user.id) {
      let message = npgettext(
        "profile username history",
        "Your username was changed %(changes)s time.",
        "Your username was changed %(changes)s times.",
        this.state.count
      )

      return interpolate(
        message,
        {
          changes: this.state.count,
        },
        true
      )
    } else {
      let message = npgettext(
        "profile username history",
        "%(username)s's username was changed %(changes)s time.",
        "%(username)s's username was changed %(changes)s times.",
        this.state.count
      )

      return interpolate(
        message,
        {
          username: this.props.profile.username,
          changes: this.state.count,
        },
        true
      )
    }
  }

  getEmptyMessage() {
    if (this.state.search) {
      return pgettext(
        "profile username history",
        "Search returned no username changes matching specified criteria."
      )
    } else if (this.props.user.id === this.props.profile.id) {
      return pgettext(
        "username history empty",
        "Your account has no history of name changes."
      )
    } else {
      return interpolate(
        pgettext(
          "profile username history",
          "%(username)s's username was never changed."
        ),
        {
          username: this.props.profile.username,
        },
        true
      )
    }
  }

  getMoreButton() {
    if (!this.state.more) return null

    return (
      <div className="pager-more">
        <Button
          className="btn btn-default btn-outline"
          loading={this.state.isBusy}
          onClick={this.loadMore}
        >
          {interpolate(
            pgettext("profile username history", "Show older (%(more)s)"),
            {
              more: this.state.more,
            },
            true
          )}
        </Button>
      </div>
    )
  }

  render() {
    return (
      <div className="profile-username-history">
        <Toolbar>
          <ToolbarSection auto>
            <ToolbarItem auto>
              <h3>{this.getLabel()}</h3>
            </ToolbarItem>
          </ToolbarSection>
          <ToolbarSection>
            <ToolbarItem>
              <Search
                value={this.state.search}
                onChange={this.search}
                placeholder={pgettext(
                  "profile username history search input",
                  "Search history..."
                )}
              />
            </ToolbarItem>
          </ToolbarSection>
        </Toolbar>

        <UsernameHistory
          isLoaded={this.state.isLoaded}
          emptyMessage={this.getEmptyMessage()}
          changes={this.props["username-history"]}
        />

        {this.getMoreButton()}
      </div>
    )
  }
}
