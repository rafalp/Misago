import { toggle } from "misago/utils/sets"

export const SELECT_ALL = "SELECT_ALL"
export const SELECT_NONE = "SELECT_NONE"
export const SELECT_ITEM = "SELECT_ITEM"

export function all(itemsIds) {
  return {
    type: SELECT_ALL,
    items: itemsIds,
  }
}

export function none() {
  return {
    type: SELECT_NONE,
  }
}

export function item(itemId) {
  return {
    type: SELECT_ITEM,
    item: itemId,
  }
}

export default function selection(state = [], action = null) {
  switch (action.type) {
    case SELECT_ALL:
      return action.items

    case SELECT_NONE:
      return []

    case SELECT_ITEM:
      return toggle(state, action.item)

    default:
      return state
  }
}
