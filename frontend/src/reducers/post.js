import moment from "moment"
import { hydrateUser } from "./users"

export const PATCH_POST = "PATCH_POST"

export function hydrate(json) {
  return Object.assign({}, json, {
    posted_on: moment(json.posted_on),
    updated_on: moment(json.updated_on),
    hidden_on: moment(json.hidden_on),

    attachments: json.attachments
      ? json.attachments.map(hydrateAttachment)
      : null,
    poster: json.poster ? hydrateUser(json.poster) : null,

    isSelected: false,
    isBusy: false,
    isDeleted: false,
  })
}

export function hydrateAttachment(json) {
  return Object.assign({}, json, {
    uploaded_on: moment(json.uploaded_on),
  })
}

export function patch(post, patch) {
  return {
    type: PATCH_POST,
    post,
    patch,
  }
}

export default function post(state = {}, action = null) {
  switch (action.type) {
    case PATCH_POST:
      if (state.id == action.post.id) {
        return Object.assign({}, state, action.patch)
      }
      return state

    default:
      return state
  }
}
