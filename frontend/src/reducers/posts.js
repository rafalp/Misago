import postReducer, { PATCH_POST, hydrate as hydratePost } from 'misago/reducers/post';

export const SELECT_POST = 'SELECT_POST';
export const DESELECT_POST = 'DESELECT_POST';
export const DESELECT_POSTS = 'DESELECT_POSTS';
export const LOAD_POSTS = 'LOAD_POSTS';
export const UNLOAD_POSTS = 'UNLOAD_POSTS';

export function select(post) {
  return {
    type: SELECT_POST,
    post
  };
}

export function deselect(post) {
  return {
    type: DESELECT_POST,
    post
  };
}

export function deselectAll() {
  return {
    type: DESELECT_POSTS,
  };
}

export function hydrate(json) {
  return Object.assign({}, json, {
    results: json.results.map(hydratePost),
    isLoaded: true,
    isBusy: false,
    isSelected: false
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
    case SELECT_POST:
      const selectedPosts = state.results.map((post) => {
        if (post.id == action.post.id) {
          return Object.assign({}, post, {
            isSelected: true
          });
        } else {
          return post;
        }
      });

      return Object.assign({}, state, {
        results: selectedPosts
      });

    case DESELECT_POST:
      const deseletedPosts = state.results.map((post) => {
        if (post.id == action.post.id) {
          return Object.assign({}, post, {
            isSelected: false
          });
        } else {
          return post;
        }
      });

      return Object.assign({}, state, {
        results: deseletedPosts
      });

    case DESELECT_POSTS:
      const deseletedAllPosts = state.results.map((post) => {
        return Object.assign({}, post, {
          isSelected: false
        });
      });

      return Object.assign({}, state, {
        results: deseletedAllPosts
      });

    case LOAD_POSTS:
      return action.state;

    case UNLOAD_POSTS:
      return Object.assign({}, state, {
        isLoaded: false,
      });

    case PATCH_POST:
      const reducedPosts = state.results.map((post) => {
        return postReducer(post, action);
      });

      return Object.assign({}, state, {
        results: reducedPosts
      });

    default:
      return state;
  }
}