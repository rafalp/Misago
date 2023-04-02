import React from "react"
import { connect } from "react-redux"
import Route from "misago/components/threads/route"
import misago from "misago/index"

export function getSelect(store) {
  return {
    selection: store.selection,
    threads: store.threads,
    tick: store.tick.tick,
    user: store.auth.user,
  }
}

export function getLists(user) {
  let lists = [
    {
      type: "all",
      path: "",
      name: gettext("All"),
      longName: gettext("All threads"),
    },
  ]

  if (user.id) {
    lists.push({
      type: "my",
      path: "my/",
      name: gettext("My"),
      longName: gettext("My threads"),
    })
    lists.push({
      type: "new",
      path: "new/",
      name: gettext("New"),
      longName: gettext("New threads"),
    })
    lists.push({
      type: "unread",
      path: "unread/",
      name: gettext("Unread"),
      longName: gettext("Unread threads"),
    })
    lists.push({
      type: "subscribed",
      path: "subscribed/",
      name: gettext("Subscribed"),
      longName: gettext("Subscribed threads"),
    })

    if (user.acl.can_see_unapproved_content_lists) {
      lists.push({
        type: "unapproved",
        path: "unapproved/",
        name: gettext("Unapproved"),
        longName: gettext("Unapproved content"),
      })
    }
  }

  return lists
}

const RouteConnected = connect(getSelect)(Route)

export function paths(user, options) {
  const categories = misago.get("CATEGORIES")
  let lists = getLists(user)

  let routes = []
  let categoriesMap = {}

  categories.forEach(function (category) {
    categoriesMap[category.id] = category

    lists.forEach(function (list) {
      const path = category.url.index + list.path
      routes.push({
        path: path === "/" ? path : path.substring(1),
        element: (
          <RouteConnected
            categories={categories}
            categoriesMap={categoriesMap}
            category={category}
            lists={lists}
            list={list}
            options={options}
          />
        ),
      })
    })
  })

  return routes
}
