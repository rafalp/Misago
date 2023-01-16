import moment from "moment"

export const BUSY_POLL = "BUSY_POLL"
export const RELEASE_POLL = "RELEASE_POLL"
export const REMOVE_POLL = "REMOVE_POLL"
export const REPLACE_POLL = "REPLACE_POLL"
export const UPDATE_POLL = "UPDATE_POLL"

export function hydrate(json) {
  let hasSelectedChoices = false
  for (const i in json.choices) {
    const choice = json.choices[i]
    if (choice.selected) {
      hasSelectedChoices = true
      break
    }
  }

  return Object.assign({}, json, {
    posted_on: moment(json.posted_on),

    hasSelectedChoices,
    endsOn: json.length
      ? moment(json.posted_on).add(json.length, "days")
      : null,

    isBusy: false,
  })
}

export function busy() {
  return {
    type: BUSY_POLL,
  }
}

export function release() {
  return {
    type: RELEASE_POLL,
  }
}

export function replace(newState, hydrated = false) {
  return {
    type: REPLACE_POLL,
    state: hydrated ? newState : hydrate(newState),
  }
}

export function update(data) {
  return {
    type: UPDATE_POLL,
    data,
  }
}

export function remove() {
  return {
    type: REMOVE_POLL,
  }
}

export default function poll(state = {}, action = null) {
  switch (action.type) {
    case BUSY_POLL:
      return Object.assign({}, state, { isBusy: true })

    case RELEASE_POLL:
      return Object.assign({}, state, { isBusy: false })

    case REMOVE_POLL:
      return {
        isBusy: false,
      }

    case REPLACE_POLL:
      return action.state

    case UPDATE_POLL:
      return Object.assign({}, state, action.data)

    default:
      return state
  }
}
