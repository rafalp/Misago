import React from "react"
import Button from "misago/components/button"
import Search from "misago/components/quick-search"
import UsersList from "misago/components/users-list"
import misago from "misago/index"
import { hydrate, append } from "misago/reducers/users"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"
import title from "misago/services/page-title"
import { Toolbar, ToolbarItem, ToolbarSection } from "../Toolbar"

export default class extends React.Component {
  constructor(props) {
    super(props)

    this.setSpecialProps()

    if (misago.has(this.PRELOADED_DATA_KEY)) {
      this.initWithPreloadedData(misago.pop(this.PRELOADED_DATA_KEY))
    } else {
      this.initWithoutPreloadedData()
    }
  }

  setSpecialProps() {
    this.PRELOADED_DATA_KEY = "PROFILE_FOLLOWERS"
    this.TITLE = pgettext("profile followers title", "Followers")
    this.API_FILTER = "followers"
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

    this.loadUsers()
  }

  loadUsers(page = 1, search = null) {
    const apiUrl = this.props.profile.api[this.API_FILTER]

    ajax
      .get(
        apiUrl,
        {
          search: search,
          page: page || 1,
        },
        "user-" + this.API_FILTER
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
      title: this.TITLE,
      parent: this.props.profile.username,
    })
  }

  loadMore = () => {
    this.setState({
      isBusy: true,
    })

    this.loadUsers(this.state.page + 1, this.state.search)
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

    this.loadUsers(1, ev.target.value)
  }

  getLabel() {
    if (!this.state.isLoaded) {
      return pgettext("Loading...")
    } else if (this.state.search) {
      let message = npgettext(
        "profile followers",
        "Found %(users)s user.",
        "Found %(users)s users.",
        this.state.count
      )

      return interpolate(
        message,
        {
          users: this.state.count,
        },
        true
      )
    } else if (this.props.profile.id === this.props.user.id) {
      let message = npgettext(
        "profile followers",
        "You have %(users)s follower.",
        "You have %(users)s followers.",
        this.state.count
      )

      return interpolate(
        message,
        {
          users: this.state.count,
        },
        true
      )
    } else {
      let message = npgettext(
        "profile followers",
        "%(username)s has %(users)s follower.",
        "%(username)s has %(users)s followers.",
        this.state.count
      )

      return interpolate(
        message,
        {
          username: this.props.profile.username,
          users: this.state.count,
        },
        true
      )
    }
  }

  getEmptyMessage() {
    if (this.state.search) {
      return pgettext(
        "profile followers",
        "Search returned no users matching specified criteria."
      )
    } else if (this.props.user.id === this.props.profile.id) {
      return pgettext("profile followers", "You have no followers.")
    } else {
      return interpolate(
        pgettext("profile followers", "%(username)s has no followers."),
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
            pgettext("profile followers", "Show more (%(more)s)"),
            {
              more: this.state.more,
            },
            true
          )}
        </Button>
      </div>
    )
  }

  getListBody() {
    if (this.state.isLoaded && this.state.count === 0) {
      return <p className="lead">{this.getEmptyMessage()}</p>
    }

    return (
      <div>
        <UsersList
          cols={3}
          isReady={this.state.isLoaded}
          users={this.props.users}
        />

        {this.getMoreButton()}
      </div>
    )
  }

  getClassName() {
    return "profile-" + this.API_FILTER
  }

  render() {
    return (
      <div className={this.getClassName()}>
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
                  "profile followers search",
                  "Search users..."
                )}
              />
            </ToolbarItem>
          </ToolbarSection>
        </Toolbar>

        {this.getListBody()}
      </div>
    )
  }
}
