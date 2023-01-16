import moment from "moment"
import { UPDATE_AVATAR, UPDATE_USERNAME } from "misago/reducers/users"
import concatUnique from "misago/utils/concat-unique"

export const ADD_NAME_CHANGE = "ADD_NAME_CHANGE"
export const APPEND_HISTORY = "APPEND_HISTORY"
export const HYDRATE_HISTORY = "HYDRATE_HISTORY"

export function addNameChange(change, user, changedBy) {
  return {
    type: ADD_NAME_CHANGE,
    change,
    user,
    changedBy,
  }
}

export function append(items) {
  return {
    type: APPEND_HISTORY,
    items: items,
  }
}

export function hydrate(items) {
  return {
    type: HYDRATE_HISTORY,
    items: items,
  }
}

export function hydrateNamechange(namechange) {
  return Object.assign({}, namechange, {
    changed_on: moment(namechange.changed_on),
  })
}

export default function username(state = [], action = null) {
  switch (action.type) {
    case ADD_NAME_CHANGE:
      let newState = state.slice()
      newState.unshift({
        id: Math.floor(Date.now() / 1000), // just small hax for getting id
        changed_by: action.changedBy,
        changed_by_username: action.changedBy.username,
        changed_on: moment(),
        new_username: action.change.username,
        old_username: action.user.username,
      })
      return newState

    case APPEND_HISTORY:
      return concatUnique(state, action.items.map(hydrateNamechange))

    case HYDRATE_HISTORY:
      return action.items.map(hydrateNamechange)

    case UPDATE_AVATAR:
      return state.map(function (item) {
        item = Object.assign({}, item)
        if (item.changed_by && item.changed_by.id === action.userId) {
          item.changed_by = Object.assign({}, item.changed_by, {
            avatars: action.avatars,
          })
        }

        return item
      })

    case UPDATE_USERNAME:
      return state.map(function (item) {
        item = Object.assign({}, item)
        if (item.changed_by && item.changed_by.id === action.userId) {
          item.changed_by = Object.assign({}, item.changed_by, {
            username: action.username,
            slug: action.slug,
          })
        }

        return Object.assign({}, item)
      })

    default:
      return state
  }
}
