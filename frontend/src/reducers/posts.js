import { hydrate as hydratePost } from 'misago/reducers/post';

export const LOAD_POSTS = 'LOAD_POSTS';
export const UNLOAD_POSTS = 'UNLOAD_POSTS';

export function hydrate(json) {
  return Object.assign({}, json, {
    results: json.results.map(hydratePost),
    isLoaded: true,
    isBusy: false
  });
}

export function load(newState, hydrated=false) {
  return {
    type: LOAD_POSTS,
    state: hydrated ? newState : hydrate(newState)
  };
}

export function unload() {
  return {
    type: UNLOAD_POSTS
  };
}

export default function posts(state={}, action=null) {
  switch (action.type) {
    case LOAD_POSTS:
      return action.state;

    case UNLOAD_POSTS:
      return Object.assign({}, state, {
        isLoaded: false,
      });

    default:
      return state;
  }
}