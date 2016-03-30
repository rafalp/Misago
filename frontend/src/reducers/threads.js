import moment from 'moment';
import concatUnique from 'misago/utils/concat-unique';

export const APPEND_THREADS = 'APPEND_THREADS';
export const HYDRATE_THREADS = 'HYDRATE_THREADS';
export const PATCH_THREADS = 'PATCH_THREADS';

export function append(items) {
 return {
    type: APPEND_THREADS,
    items
  };
}

export function hydrate(items) {
  return {
    type: HYDRATE_THREADS,
    items
  };
}

export function patch(thread, patch) {
  return {
    type: PATCH_THREADS,
    thread,
    patch
  };
}

export function hydrateThread(thread) {
  return Object.assign({}, thread, {
    started_on: moment(thread.started_on),
    last_post_on: moment(thread.last_post_on)
  });
}

export default function thread(state=[], action=null) {
  switch (action.type) {
    case APPEND_THREADS:
      let mergedState = concatUnique(action.items.map(hydrateThread), state);
      return mergedState.sort(function(a, b) {
        if (a.last_post > b.last_post) {
          return -1;
        } else if (a.last_post < b.last_post) {
          return 1;
        } else {
          return 0;
        }
      });

    case HYDRATE_THREADS:
      return action.items.map(hydrateThread);

    case PATCH_THREADS:
      return state.map(function(item) {
        if (item.id === action.thread.id) {
          return Object.assign({}, item, action.patch);
        } else {
          return item;
        }
      });

    default:
      return state;
  }
}