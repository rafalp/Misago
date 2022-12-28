import { connect } from "react-redux"
import SearchThreads from "./threads"
import SearchUsers from "./users"

const components = {
  threads: SearchThreads,
  users: SearchUsers,
}

export function select(store) {
  return {
    posts: store.posts,
    search: store.search,
    tick: store.tick.tick,
    user: store.auth.user,
    users: store.users,
  }
}

export default function (providers) {
  return providers.map((provider) => {
    return {
      path: provider.url,
      component: connect(select)(components[provider.id]),
      provider: provider,
    }
  })
}
