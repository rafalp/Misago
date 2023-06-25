import moment from "moment"
import React from "react"
import * as post from "misago/reducers/post"
import * as posts from "misago/reducers/posts"
import ajax from "misago/services/ajax"
import modal from "misago/services/modal"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"
import ErrorsList from "./errors-list"

export function approve(props) {
  const { selection } = props

  const ops = [{ op: "replace", path: "is-unapproved", value: false }]

  const newState = selection.map((post) => {
    return {
      id: post.id,
      is_unapproved: false,
    }
  })

  const previousState = selection.map((post) => {
    return {
      id: post.id,
      is_unapproved: post.is_unapproved,
    }
  })

  patch(props, ops, newState, previousState)
}

export function protect(props) {
  const { selection } = props

  const ops = [{ op: "replace", path: "is-protected", value: true }]

  const newState = selection.map((post) => {
    return {
      id: post.id,
      is_protected: true,
    }
  })

  const previousState = selection.map((post) => {
    return {
      id: post.id,
      is_protected: post.is_protected,
    }
  })

  patch(props, ops, newState, previousState)
}

export function unprotect(props) {
  const { selection } = props

  const ops = [{ op: "replace", path: "is-protected", value: false }]

  const newState = selection.map((post) => {
    return {
      id: post.id,
      is_protected: false,
    }
  })

  const previousState = selection.map((post) => {
    return {
      id: post.id,
      is_protected: post.is_protected,
    }
  })

  patch(props, ops, newState, previousState)
}

export function hide(props) {
  const { selection } = props

  const ops = [{ op: "replace", path: "is-hidden", value: true }]

  const newState = selection.map((post) => {
    return {
      id: post.id,
      is_hidden: true,
      hidden_on: moment(),
      hidden_by_name: props.user.username,
      url: Object.assign(post.url, {
        hidden_by: props.user.url,
      }),
    }
  })

  const previousState = selection.map((post) => {
    return {
      id: post.id,
      is_hidden: post.is_hidden,
      hidden_on: post.hidden_on,
      hidden_by_name: post.hidden_by_name,
      url: post.url,
    }
  })

  patch(props, ops, newState, previousState)
}

export function unhide(props) {
  const { selection } = props

  const ops = [{ op: "replace", path: "is-hidden", value: false }]

  const newState = selection.map((post) => {
    return {
      id: post.id,
      is_hidden: false,
      hidden_on: moment(),
      hidden_by_name: props.user.username,
      url: Object.assign(post.url, {
        hidden_by: props.user.url,
      }),
    }
  })

  const previousState = selection.map((post) => {
    return {
      id: post.id,
      is_hidden: post.is_hidden,
      hidden_on: post.hidden_on,
      hidden_by_name: post.hidden_by_name,
      url: post.url,
    }
  })

  patch(props, ops, newState, previousState)
}

export function patch(props, ops, newState, previousState) {
  const { selection, thread } = props

  // patch selected items
  newState.forEach((item) => {
    post.patch(item, item)
  })

  // deselect all the things
  store.dispatch(posts.deselectAll())

  // call ajax
  const data = {
    ops,

    ids: selection.map((post) => {
      return post.id
    }),
  }

  ajax.patch(thread.api.posts.index, data).then(
    (data) => {
      data.forEach((item) => {
        store.dispatch(post.patch(item, item))
      })
    },
    (rejection) => {
      if (rejection.status !== 400) {
        // rollback all
        previousState.forEach((item) => {
          store.dispatch(post.patch(item, item))
        })
        return snackbar.apiError(rejection)
      }

      let errors = []
      let rollback = []

      rejection.forEach((item) => {
        if (item.detail) {
          errors.push(item)
          rollback.push(item.id)
        } else {
          store.dispatch(post.patch(item, item))
        }

        previousState.forEach((item) => {
          if (rollback.indexOf(item) !== -1) {
            store.dispatch(post.patch(item, item))
          }
        })
      })

      let posts = {}
      selection.forEach((item) => {
        posts[item.id] = item
      })

      modal.show(<ErrorsList errors={errors} posts={posts} />)
    }
  )
}

export function merge(props) {
  let confirmed = window.confirm(
    pgettext(
      "merge posts",
      "Are you sure you want to merge selected posts? This action is not reversible!"
    )
  )
  if (!confirmed) {
    return
  }

  props.selection.slice(1).map((selection) => {
    store.dispatch(
      post.patch(selection, {
        isDeleted: true,
      })
    )
  })

  ajax
    .post(props.thread.api.posts.merge, {
      posts: props.selection.map((post) => post.id),
    })
    .then(
      (data) => {
        store.dispatch(post.patch(data, post.hydrate(data)))
      },
      (rejection) => {
        if (rejection.status === 400) {
          snackbar.error(rejection.detail)
        } else {
          snackbar.apiError(rejection)
        }

        props.selection.slice(1).map((selection) => {
          store.dispatch(
            post.patch(selection, {
              isDeleted: false,
            })
          )
        })
      }
    )

  store.dispatch(posts.deselectAll())
}

export function remove(props) {
  let confirmed = window.confirm(
    pgettext(
      "delete posts",
      "Are you sure you want to delete selected posts? This action is not reversible!"
    )
  )
  if (!confirmed) {
    return
  }

  props.selection.map((selection) => {
    store.dispatch(
      post.patch(selection, {
        isDeleted: true,
      })
    )
  })

  const ids = props.selection.map((post) => {
    return post.id
  })

  ajax.delete(props.thread.api.posts.index, ids).then(
    () => {
      return
    },
    (rejection) => {
      if (rejection.status === 400) {
        snackbar.error(rejection.detail)
      } else {
        snackbar.apiError(rejection)
      }

      props.selection.map((selection) => {
        store.dispatch(
          post.patch(selection, {
            isDeleted: false,
          })
        )
      })
    }
  )

  store.dispatch(posts.deselectAll())
}
