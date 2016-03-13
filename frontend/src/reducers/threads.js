export const APPEND_THREADS = 'APPEND_THREADS';
export const HYDRATE_THREADS = 'HYDRATE_THREADS';

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

export function hydrateThread(thread) {
  return Object.assign({}, thread);
}

export default function thread(state=[], action=null) {
  switch (action.type) {
    case APPEND_THREADS:
      return state.concat(action.items.map(hydrateThread));

    case HYDRATE_THREADS:
      return action.items.map(hydrateThread);

    default:
      return state;
  }
}