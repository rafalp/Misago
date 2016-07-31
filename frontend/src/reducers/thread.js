import moment from 'moment';

export const REPLACE_THREAD = 'REPLACE_THREAD';

export function hydrate(json) {
  return Object.assign({}, json, {
    started_on: moment(json.started_on),
    last_post_on: moment(json.last_post_on),

    isBusy: false
  });
}

export function replace(newState, hydrated=false) {
  return {
    type: REPLACE_THREAD,
    state: hydrated ? newState : hydrate(newState)
  };
}

export default function thread(state={}, action=null) {
  switch (action.type) {
    case REPLACE_THREAD:
      return action.state;

    default:
      return state;
  }
}