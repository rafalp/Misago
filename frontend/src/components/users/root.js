import React from "react"
import { connect } from "react-redux"
import ActivePosters from "misago/components/users/active-posters/root"
import Rank from "misago/components/users/rank/root"
import WithDropdown from "misago/components/with-dropdown"
import misago from "misago/index"
import {
  PageHeader,
  PageHeaderBanner,
  PageHeaderContainer,
} from "../PageHeader"

export default class extends WithDropdown {
  render() {
    return (
      <div className="page page-users-lists">
        <PageHeaderContainer>
          <PageHeader styleName="users-lists">
            <PageHeaderBanner styleName="users-lists">
              <h1>{pgettext("users page title", "Users")}</h1>
            </PageHeaderBanner>
          </PageHeader>
        </PageHeaderContainer>
        {this.props.children}
      </div>
    )
  }
}

export function select(store) {
  return {
    tick: store.tick.tick,
    user: store.auth.user,
    users: store.users,
  }
}

export function paths() {
  let paths = []

  misago.get("USERS_LISTS").forEach(function (item) {
    if (item.component === "rank") {
      paths.push({
        path: misago.get("USERS_LIST_URL") + item.slug + "/:page/",
        component: connect(select)(Rank),
        rank: item,
      })
      paths.push({
        path: misago.get("USERS_LIST_URL") + item.slug + "/",
        component: connect(select)(Rank),
        rank: item,
      })
    } else if (item.component === "active-posters") {
      paths.push({
        path: misago.get("USERS_LIST_URL") + item.component + "/",
        component: connect(select)(ActivePosters),
        extra: {
          name: item.name,
        },
      })
    }
  })

  return paths
}
