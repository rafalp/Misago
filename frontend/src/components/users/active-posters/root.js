import React from "react"
import ListEmpty from "misago/components/users/active-posters/list-empty"
import ListPreview from "misago/components/users/active-posters/list-preview"
import ListReady from "misago/components/users/active-posters/list-ready"
import misago from "misago/index"
import { hydrate } from "misago/reducers/users"
import polls from "misago/services/polls"
import store from "misago/services/store"
import title from "misago/services/page-title"

export default class extends React.Component {
  constructor(props) {
    super(props)

    if (misago.has("USERS")) {
      this.initWithPreloadedData(misago.pop("USERS"))
    } else {
      this.initWithoutPreloadedData()
    }

    this.startPolling()
  }

  initWithPreloadedData(data) {
    this.state = {
      isLoaded: true,

      trackedPeriod: data.tracked_period,
      count: data.count,
    }

    store.dispatch(hydrate(data.results))
  }

  initWithoutPreloadedData() {
    this.state = {
      isLoaded: false,
    }
  }

  startPolling() {
    polls.start({
      poll: "active-posters",
      url: misago.get("USERS_API"),
      data: {
        list: "active",
      },
      frequency: 90 * 1000,
      update: this.update,
    })
  }

  update = (data) => {
    store.dispatch(hydrate(data.results))

    this.setState({
      isLoaded: true,

      trackedPeriod: data.tracked_period,
      count: data.count,
    })
  }

  componentDidMount() {
    title.set({
      title: this.props.route.extra.name,
      parent: gettext("Users"),
    })
  }

  componentWillUnmount() {
    polls.stop("active-posters")
  }

  render() {
    if (this.state.isLoaded) {
      if (this.state.count > 0) {
        return (
          <ListReady
            users={this.props.users}
            trackedPeriod={this.state.trackedPeriod}
            count={this.state.count}
          />
        )
      } else {
        return <ListEmpty trackedPeriod={this.state.trackedPeriod} />
      }
    } else {
      return <ListPreview />
    }
  }
}
