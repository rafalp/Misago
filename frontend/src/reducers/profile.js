import moment from "moment"
import {
  UPDATE_AVATAR,
  UPDATE_USERNAME,
  hydrateStatus,
} from "misago/reducers/users"

export const HYDRATE_PROFILE = "HYDRATE_PROFILE"
export const PATCH_PROFILE = "PATCH_PROFILE"

export function hydrate(profile) {
  return {
    type: HYDRATE_PROFILE,
    profile,
  }
}

export function patch(patch) {
  return {
    type: PATCH_PROFILE,
    patch,
  }
}

export default function auth(state = {}, action = null) {
  switch (action.type) {
    case HYDRATE_PROFILE:
      return Object.assign({}, action.profile, {
        joined_on: moment(action.profile.joined_on),
        status: hydrateStatus(action.profile.status),
      })

    case PATCH_PROFILE:
      return Object.assign({}, state, action.patch)

    case UPDATE_AVATAR:
      if (state.id === action.userId) {
        return Object.assign({}, state, {
          avatars: action.avatars,
        })
      }
      return state

    case UPDATE_USERNAME:
      if (state.id === action.userId) {
        return Object.assign({}, state, {
          username: action.username,
          slug: action.slug,
        })
      }
      return state

    default:
      return state
  }
}
