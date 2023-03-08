import React from "react"
import { connect } from "react-redux"
import BanDetails from "./ban-details"
import Details from "./details"
import { Posts, Threads } from "./feed"
import Followers from "./followers"
import Follows from "./follows"
import UsernameHistory from "./username-history"
import WithDropdown from "misago/components/with-dropdown"
import misago from "misago"
import { hydrate } from "misago/reducers/profile"
import polls from "misago/services/polls"
import store from "misago/services/store"
import PageContainer from "../PageContainer"
import ProfileHeader from "./ProfileHeader"
import ProfileNav from "./ProfileNav"

export default class extends WithDropdown {
  constructor(props) {
    super(props)

    this.startPolling(props.profile.api.index)
  }

  startPolling(api) {
    polls.start({
      poll: "user-profile",
      url: api,
      frequency: 90 * 1000,
      update: this.update,
    })
  }

  update = (data) => {
    store.dispatch(hydrate(data))
  }

  render() {
    const baseUrl = misago.get("PROFILE").url
    const pages = misago.get("PROFILE_PAGES")
    const page = pages.filter((page) => {
      const url = baseUrl + page.component + "/"
      return this.props.location.pathname === url
    })[0]
    const { profile, user } = this.props
    const moderation = getModeration(profile, user)
    const message =
      !!user.acl.can_start_private_threads && profile.id !== user.id
    const follow = !!profile.acl.can_follow && profile.id !== user.id

    return (
      <div className="page page-user-profile">
        <ProfileHeader
          profile={this.props.profile}
          user={this.props.user}
          moderation={moderation}
          message={message}
          follow={follow}
        />
        <PageContainer>
          <ProfileNav baseUrl={baseUrl} page={page} pages={pages} />

          {this.props.children}
        </PageContainer>
      </div>
    )
  }
}

const getModeration = (profile, user) => {
  const moderation = {
    available: false,
    rename: false,
    avatar: false,
    delete: false,
  }

  if (user.is_anonymous) return moderation

  moderation.rename = profile.acl.can_rename
  moderation.avatar = profile.acl.can_moderate_avatar
  moderation.delete = profile.acl.can_delete
  moderation.available = !!(
    moderation.rename ||
    moderation.avatar ||
    moderation.delete
  )

  return moderation
}

export function select(store) {
  return {
    isAuthenticated: store.auth.user.id === store.profile.id,

    tick: store.tick.tick,
    user: store.auth.user,
    users: store.users,
    posts: store.posts,
    profile: store.profile,
    profileDetails: store["profile-details"],
    "username-history": store["username-history"],
  }
}

const COMPONENTS = {
  posts: Posts,
  threads: Threads,
  followers: Followers,
  follows: Follows,
  details: Details,
  "username-history": UsernameHistory,
  "ban-details": BanDetails,
}

export function paths() {
  let paths = []
  misago.get("PROFILE_PAGES").forEach(function (item) {
    paths.push(
      Object.assign({}, item, {
        path: misago.get("PROFILE").url + item.component + "/",
        component: connect(select)(COMPONENTS[item.component]),
      })
    )
  })

  return paths
}
