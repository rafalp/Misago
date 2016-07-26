import { hydrate as hydratePost } from 'misago/reducers/post';

export const REPLACE_POSTS = 'REPLACE_POSTS';

export function replace(newState, hydrate=true) {
  return {
    type: REPLACE_POSTS,
    state: hydrate ? hydrate(newState) : newState
  };
}

export function hydrate(json) {
  return Object.assign({}, json, {
    results: json.results.map(hydratePost),
    isLoaded: true,
    isBusy: false
  });
}

export default function posts(state={}, action=null) {
  switch (action.type) {
    default:
      return state;
  }
}