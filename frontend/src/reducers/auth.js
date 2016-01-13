import { UPDATE_AVATAR } from 'misago/reducers/users';

export var initialState = {
  signedIn: false,
  signedOut: false
};

export const SIGN_IN = 'SIGN_IN';
export const SIGN_OUT = 'SIGN_OUT';

export function signIn(user) {
  return {
    type: SIGN_IN,
    user
  };
}

export function signOut(soft=false) {
  return {
    type: SIGN_OUT,
    soft
  };
}

export default function auth(state=initialState, action=null) {
  switch (action.type) {
    case SIGN_IN:
      return Object.assign({}, state, {
        signedIn: action.user
      });

    case SIGN_OUT:
      return Object.assign({}, state, {
        isAuthenticated: false,
        isAnonymous: true,
        signedOut: !action.soft
      });

    case UPDATE_AVATAR:
      if (state.isAuthenticated && state.user.id === action.userId) {
        let newState = Object.assign({}, state);
        newState.user = Object.assign({}, state.user, {
          'avatar_hash': action.avatarHash
        });
        return newState;
      }
      return state;

    default:
      return state;
  }
}
