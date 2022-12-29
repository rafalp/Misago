export const REPLACE_SEARCH = "REPLACE_SEARCH"
export const UPDATE_SEARCH = "UPDATE_SEARCH"
export const UPDATE_SEARCH_PROVIDER = "UPDATE_SEARCH_PROVIDER"

export const initialState = {
  isLoading: false,
  query: "",
  providers: [],
}

export function replace(newState) {
  return {
    type: REPLACE_SEARCH,
    state: {
      isLoading: false,
      providers: newState,
    },
  }
}

export function update(newState) {
  return {
    type: UPDATE_SEARCH,
    update: newState,
  }
}

export function updateProvider(provider) {
  return {
    type: UPDATE_SEARCH_PROVIDER,
    provider: provider,
  }
}

export default function participants(state = {}, action = null) {
  switch (action.type) {
    case REPLACE_SEARCH:
      return action.state

    case UPDATE_SEARCH:
      return Object.assign({}, state, action.update)

    case UPDATE_SEARCH_PROVIDER:
      return Object.assign({}, state, {
        providers: state.providers.map((provider) => {
          if (provider.id === action.provider.id) {
            return action.provider
          } else {
            return provider
          }
        }),
      })

    default:
      return state
  }
}
