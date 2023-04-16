import { UPDATE_AVATAR, UPDATE_USERNAME } from "misago/reducers/users"

export var initialState = {
  signedIn: false,
  signedOut: false,
}

export const UPDATE_AUTHENTICATED_USER = "UPDATE_AUTHENTICATED_USER"
export const PATCH_USER = "PATCH_USER"
export const SIGN_IN = "SIGN_IN"
export const SIGN_OUT = "SIGN_OUT"

export function updateAuthenticatedUser(data) {
  return {
    type: UPDATE_AUTHENTICATED_USER,
    data,
  }
}

export function patch(patch) {
  return {
    type: PATCH_USER,
    patch,
  }
}

export function signIn(user) {
  return {
    type: SIGN_IN,
    user,
  }
}

export function signOut(soft = false) {
  return {
    type: SIGN_OUT,
    soft,
  }
}

export default function auth(state = initialState, action = null) {
  switch (action.type) {
    case PATCH_USER:
      let newState = Object.assign({}, state)
      newState.user = Object.assign({}, state.user, action.patch)
      return newState

    case UPDATE_AUTHENTICATED_USER:
      let updatedState = Object.assign({}, state)
      updatedState.user = Object.assign({}, state.user, action.data)
      return updatedState

    case SIGN_IN:
      return Object.assign({}, state, {
        signedIn: action.user,
      })

    case SIGN_OUT:
      return Object.assign({}, state, {
        isAuthenticated: false,
        isAnonymous: true,
        signedOut: !action.soft,
      })

    case UPDATE_AVATAR:
      if (state.isAuthenticated && state.user.id === action.userId) {
        let newState = Object.assign({}, state)
        newState.user = Object.assign({}, state.user, {
          avatars: action.avatars,
        })
        return newState
      }
      return state

    case UPDATE_USERNAME:
      if (state.isAuthenticated && state.user.id === action.userId) {
        let newState = Object.assign({}, state)
        newState.user = Object.assign({}, state.user, {
          username: action.username,
          slug: action.slug,
        })
        return newState
      }
      return state

    default:
      return state
  }
}
