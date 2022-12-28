export const LOAD_DETAILS = "LOAD_DETAILS"

export function load(newState) {
  return {
    type: LOAD_DETAILS,

    newState,
  }
}

export default function details(state = {}, action = null) {
  switch (action.type) {
    case LOAD_DETAILS:
      return action.newState

    default:
      return state
  }
}
