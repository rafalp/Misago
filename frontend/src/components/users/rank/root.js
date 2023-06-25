import React from "react"
import PageLead from "misago/components/page-lead"
import misago from "misago/index"
import { hydrate } from "misago/reducers/users"
import polls from "misago/services/polls"
import store from "misago/services/store"
import title from "misago/services/page-title"
import PageContainer from "../../PageContainer"
import RankUsersList from "./RankUsersList"
import RankUsersListLoader from "./RankUsersListLoader"
import RankUsersToolbar from "./RankUsersToolbar"
import UsersNav from "../UsersNav"

export default class extends React.Component {
  constructor(props) {
    super(props)

    if (misago.has("USERS")) {
      this.initWithPreloadedData(misago.pop("USERS"))
    } else {
      this.initWithoutPreloadedData()
    }

    this.startPolling(props.params.page || 1)
  }

  initWithPreloadedData(data) {
    this.state = Object.assign(data, {
      isLoaded: true,
    })
    store.dispatch(hydrate(data.results))
  }

  initWithoutPreloadedData() {
    this.state = {
      isLoaded: false,
    }
  }

  startPolling(page) {
    polls.start({
      poll: "rank-users",
      url: misago.get("USERS_API"),
      data: {
        rank: this.props.route.rank.id,
        page: page,
      },
      frequency: 90 * 1000,
      update: this.update,
    })
  }

  update = (data) => {
    store.dispatch(hydrate(data.results))

    data.isLoaded = true
    this.setState(data)
  }

  componentDidMount() {
    title.set({
      title: this.props.route.rank.name,
      page: this.props.params.page || null,
      parent: pgettext("users page title", "Users"),
    })
  }

  componentWillUnmount() {
    polls.stop("rank-users")
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.params.page !== nextProps.params.page) {
      title.set({
        title: this.props.route.rank.name,
        page: nextProps.params.page || null,
        parent: pgettext("users page title", "Users"),
      })

      this.setState({
        isLoaded: false,
      })

      polls.stop("rank-users")
      this.startPolling(nextProps.params.page)
    }
  }

  getClassName() {
    if (this.props.route.rank.css_class) {
      return "rank-users-list rank-users-" + this.props.route.rank.css_class
    } else {
      return "rank-users-list"
    }
  }

  getRankDescription() {
    if (this.props.route.rank.description) {
      return (
        <div className="rank-description">
          <PageLead copy={this.props.route.rank.description.html} />
        </div>
      )
    } else {
      return null
    }
  }

  getComponent() {
    if (this.state.isLoaded) {
      if (this.state.count > 0) {
        return <RankUsersList users={this.props.users} />
      } else {
        return (
          <p className="lead">
            {pgettext(
              "rank users list",
              "There are no users with this rank at the moment."
            )}
          </p>
        )
      }
    } else {
      return <RankUsersListLoader />
    }
  }

  render() {
    return (
      <div className={this.getClassName()}>
        <PageContainer>
          <UsersNav
            baseUrl={misago.get("USERS_LIST_URL")}
            page={{ name: this.props.route.rank.name }}
            pages={misago.get("USERS_LISTS")}
          />
          {this.getRankDescription()}
          {this.getComponent()}
          <RankUsersToolbar
            baseUrl={
              misago.get("USERS_LIST_URL") + this.props.route.rank.slug + "/"
            }
            users={this.state}
          />
        </PageContainer>
      </div>
    )
  }
}
