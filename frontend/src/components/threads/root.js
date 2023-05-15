import { connect } from "react-redux"
import Route from "misago/components/threads/route"
import misago from "misago/index"

export function getSelect(options) {
  return function (store) {
    return {
      options: options,
      selection: store.selection,
      threads: store.threads,
      tick: store.tick.tick,
      user: store.auth.user,
    }
  }
}

export function getLists(user) {
  let lists = [
    {
      type: "all",
      path: "",
      name: pgettext("threads list", "All"),
      longName: gettext("All threads"),
    },
  ]

  if (user.id) {
    lists.push({
      type: "my",
      path: "my/",
      name: pgettext("threads list", "My"),
      longName: pgettext("threads list", "My threads"),
    })
    lists.push({
      type: "new",
      path: "new/",
      name: pgettext("threads list", "New"),
      longName: pgettext("threads list", "New threads"),
    })
    lists.push({
      type: "unread",
      path: "unread/",
      name: pgettext("threads list", "Unread"),
      longName: pgettext("threads list", "Unread threads"),
    })
    lists.push({
      type: "watched",
      path: "watched/",
      name: pgettext("threads list", "Watched"),
      longName: pgettext("threads list", "Watched threads"),
    })

    if (user.acl.can_see_unapproved_content_lists) {
      lists.push({
        type: "unapproved",
        path: "unapproved/",
        name: pgettext("threads list", "Unapproved"),
        longName: pgettext("threads list", "Unapproved content"),
      })
    }
  }

  return lists
}

export function paths(user, mode) {
  let lists = getLists(user)
  let routes = []
  let categoriesMap = {}

  misago.get("CATEGORIES").forEach(function (category) {
    lists.forEach(function (list) {
      categoriesMap[category.id] = category

      routes.push({
        path: category.url.index + list.path,
        component: connect(getSelect(mode))(Route),

        categories: misago.get("CATEGORIES"),
        categoriesMap,
        category,

        lists,
        list,
      })
    })
  })

  return routes
}
