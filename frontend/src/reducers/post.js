import moment from 'moment';

export function hydrate(json) {
  return Object.assign({}, json, {
    posted_on: moment(json.posted_on),
    updated_on: moment(json.updated_on),
    hidden_on: moment(json.hidden_on),

    selected: false,
    busy: false
  });
}