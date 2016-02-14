import moment from 'moment';
import { UPDATE_AVATAR, UPDATE_USERNAME, dehydrateStatus } from 'misago/reducers/users';

export const DEHYDRATE_PROFILE = 'DEHYDRATE_PROFILE';
export const PATCH_PROFILE = 'PATCH_PROFILE';

export function dehydrate(profile) {
  return {
    type: DEHYDRATE_PROFILE,
    profile
  };
}

export function patchProfile(patch) {
  return {
    type: PATCH_PROFILE,
    patch
  };
}

export default function auth(state={}, action=null) {
  switch (action.type) {
    case DEHYDRATE_PROFILE:
      return Object.assign({}, action.profile, {
        joined_on: moment(action.profile.joined_on),
        status: dehydrateStatus(action.profile.status)
      });

    case PATCH_PROFILE:
      return Object.assign({}, state, action.patch);

    case UPDATE_AVATAR:
      if (state.id === action.userId) {
        return Object.assign({}, state, {
          avatar_hash: action.avatarHash
        });
      }
      return state;

    case UPDATE_USERNAME:
      if (state.id === action.userId) {
        return Object.assign({}, state, {
          username: action.username,
          slug: action.slug
        });
      }
      return state;

    default:
      return state;
  }
}
