import moment from "moment"

export function hydrateEdit(json) {
  return Object.assign({}, json, {
    edited_on: moment(json.edited_on),
  })
}
