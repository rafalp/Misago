import moment from 'moment';
import concatUnique from 'misago/utils/concat-unique';

export const APPEND_THREADS = 'APPEND_THREADS';
export const HYDRATE_THREADS = 'HYDRATE_THREADS';
export const PATCH_THREAD = 'PATCH_THREAD';
export const READ_THREADS = 'READ_THREADS';
export const SORT_THREADS = 'SORT_THREADS';

export const MODERATION_PERMISSIONS = [
  'can_announce',
  'can_close',
  'can_hide',
  'can_move',
  'can_pin',
  'can_review'
];

export function append(items, sorting) {
 return {
    type: APPEND_THREADS,
    items,
    sorting
  };
}

export function hydrate(items) {
  return {
    type: HYDRATE_THREADS,
    items
  };
}

export function patch(thread, patch, sorting=null) {
  return {
    type: PATCH_THREAD,
    thread,
    patch,
    sorting
  };
}

export function read() {
  return {
    type: READ_THREADS
  };
}

export function sort(sorting) {
  return {
    type: SORT_THREADS,
    sorting
  };
}

export function getThreadModerationOptions(thread_acl) {
  let options = [];
  MODERATION_PERMISSIONS.forEach(function(perm) {
    if (thread_acl[perm]) {
      options.push(perm);
    }
  });
  return options;
}

export function hydrateThread(thread) {
  return Object.assign({}, thread, {
    started_on: moment(thread.started_on),
    last_post_on: moment(thread.last_post_on),
    moderation: getThreadModerationOptions(thread.acl)
  });
}

export default function thread(state=[], action=null) {
  switch (action.type) {
    case APPEND_THREADS:
      const mergedState = concatUnique(action.items.map(hydrateThread), state);
      return mergedState.sort(action.sorting);

    case HYDRATE_THREADS:
      return action.items.map(hydrateThread);

    case PATCH_THREAD:
      const patchedState = state.map(function(item) {
        if (item.id === action.thread.id) {
          return Object.assign({}, item, action.patch);
        } else {
          return item;
        }
      });

      if (action.sorting) {
        return patchedState.sort(action.sorting);
      }
      return patchedState;

    case READ_THREADS:
      return state.map(function(item) {
        return Object.assign({}, item, {
          is_read: true
        });
      });

    case SORT_THREADS:
      return state.sort(action.sorting);

    default:
      return state;
  }
}