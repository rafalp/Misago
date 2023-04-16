export const OPEN = "OPEN_NOTIFICATIONS"
export const CLOSE = "CLOSE_NOTIFICATIONS"

export function open() {
  return { type: OPEN }
}

export function close() {
  return { type: CLOSE }
}

export const initialState = {
  open: false,
}

export default function notifications(state = initialState, action = null) {
  switch (action.type) {
    case OPEN:
      return Object.assign({}, state, { open: true })

    case CLOSE:
      return Object.assign({}, state, { open: false })

    default:
      return state
  }
}
