import moment from "moment"
import { REMOVE_POLL, REPLACE_POLL } from "./poll"

export const BUSY_THREAD = "BUSY_THREAD"
export const RELEASE_THREAD = "RELEASE_THREAD"
export const REPLACE_THREAD = "REPLACE_THREAD"
export const UPDATE_THREAD = "UPDATE_THREAD"
export const UPDATE_THREAD_ACL = "UPDATE_THREAD_ACL"

export function hydrate(json) {
  return Object.assign({}, json, {
    started_on: moment(json.started_on),
    last_post_on: moment(json.last_post_on),
    best_answer_marked_on: json.best_answer_marked_on
      ? moment(json.best_answer_marked_on)
      : null,

    isBusy: false,
  })
}

export function busy() {
  return {
    type: BUSY_THREAD,
  }
}

export function release() {
  return {
    type: RELEASE_THREAD,
  }
}

export function replace(newState, hydrated = false) {
  return {
    type: REPLACE_THREAD,
    state: hydrated ? newState : hydrate(newState),
  }
}

export function update(data) {
  return {
    type: UPDATE_THREAD,
    data,
  }
}

export function updateAcl(data) {
  return {
    type: UPDATE_THREAD_ACL,
    data,
  }
}

export default function thread(state = {}, action = null) {
  switch (action.type) {
    case BUSY_THREAD:
      return Object.assign({}, state, { isBusy: true })

    case RELEASE_THREAD:
      return Object.assign({}, state, { isBusy: false })

    case REMOVE_POLL:
      return Object.assign({}, state, { poll: null })

    case REPLACE_POLL:
      return Object.assign({}, state, { poll: action.state })

    case REPLACE_THREAD:
      return action.state

    case UPDATE_THREAD:
      return Object.assign({}, state, action.data)

    case UPDATE_THREAD_ACL:
      const acl = Object.assign({}, state.acl, action.data)
      return Object.assign({}, state, { acl })

    default:
      return state
  }
}
