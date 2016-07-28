import moment from 'moment';

export const REPLACE_THREAD = 'REPLACE_THREAD';

export function replace(newState, hydrate=true) {
  return {
    type: REPLACE_THREAD,
    state: hydrate ? hydrate(newState) : newState
  };
}

export function hydrate(json) {
  return Object.assign({}, json, {
    started_on: moment(json.started_on),
    last_post_on: moment(json.last_post_on),

    isBusy: false
  });
}

export default function thread(state={}, action=null) {
  switch (action.type) {
    default:
      return state;
  }
}