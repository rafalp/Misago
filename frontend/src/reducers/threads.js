export const HYDRATE_THREADS = 'HYDRATE_THREADS';

export function hydrate(items) {
  return {
    type: HYDRATE_THREADS,
    items
  };
}

export default function thread(state=[], action=null) {
  switch (action.type) {
    case HYDRATE_THREADS:
      return action.items.map(function(item) {
        return Object.assign({}, item);
      });

    default:
      return state;
  }
}