export const REPLACE_PARTICIPANTS = "REPLACE_PARTICIPANTS"

export function replace(newState) {
  return {
    type: REPLACE_PARTICIPANTS,
    state: newState,
  }
}

export default function participants(state = [], action = null) {
  switch (action.type) {
    case REPLACE_PARTICIPANTS:
      return action.state

    default:
      return state
  }
}
