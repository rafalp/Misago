import moment from 'moment';

export const BUSY_THREAD = 'BUSY_THREAD';
export const RELEASE_THREAD = 'RELEASE_THREAD';
export const REPLACE_THREAD = 'REPLACE_THREAD';
export const UPDATE_THREAD = 'UPDATE_THREAD';

export function hydrate(json) {
  return Object.assign({}, json, {
    started_on: moment(json.started_on),
    last_post_on: moment(json.last_post_on),

    isBusy: false
  });
}

export function busy() {
  return {
    type: BUSY_THREAD
  };
}

export function release() {
  return {
    type: RELEASE_THREAD
  };
}

export function replace(newState, hydrated=false) {
  return {
    type: REPLACE_THREAD,
    state: hydrated ? newState : hydrate(newState)
  };
}

export function update(data) {
  return {
    type: UPDATE_THREAD,
    data
  };
}


export default function thread(state={}, action=null) {
  switch (action.type) {
    case BUSY_THREAD:
      return Object.assign({}, state, {isBusy: true});

    case RELEASE_THREAD:
      return Object.assign({}, state, {isBusy: false});

    case REPLACE_THREAD:
      return action.state;

    case UPDATE_THREAD:
      return Object.assign({}, state, action.data);

    default:
      return state;
  }
}