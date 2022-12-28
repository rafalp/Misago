export var initialState = {
  type: "info",
  message: "",
  isVisible: false,
}

export const SHOW_SNACKBAR = "SHOW_SNACKBAR"
export const HIDE_SNACKBAR = "HIDE_SNACKBAR"

export function showSnackbar(message, type) {
  return {
    type: SHOW_SNACKBAR,
    message,
    messageType: type,
  }
}

export function hideSnackbar() {
  return {
    type: HIDE_SNACKBAR,
  }
}

export default function snackbar(state = initialState, action = null) {
  if (action.type === SHOW_SNACKBAR) {
    return {
      type: action.messageType,
      message: action.message,
      isVisible: true,
    }
  } else if (action.type === HIDE_SNACKBAR) {
    return Object.assign({}, state, {
      isVisible: false,
    })
  } else {
    return state
  }
}
