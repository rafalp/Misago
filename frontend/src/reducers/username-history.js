import { UPDATE_AVATAR, UPDATE_USERNAME } from 'misago/reducers/users';

import moment from 'moment';

export const ADD_NAME_CHANGE = 'ADD_NAME_CHANGE';
export const DEHYDRATE_RESULT = 'DEHYDRATE_RESULT';

export function addNameChange(change, user, changedBy) {
  return {
    type: ADD_NAME_CHANGE,
    change,
    user,
    changedBy
  };
}

export function dehydrate(items) {
  return {
    type: DEHYDRATE_RESULT,
    items: items
  };
}

export default function username(state=[], action=null) {
  switch (action.type) {
    case ADD_NAME_CHANGE:
      let newState = state.slice();
      newState.unshift({
        id: Math.floor(Date.now() / 1000), // just small hax for getting id
        changed_by: action.changedBy,
        changed_by_username: action.changedBy.username,
        changed_on: moment(),
        new_username: action.change.username,
        old_username: action.user.username
      });
      return newState;

    case DEHYDRATE_RESULT:
      return action.items.map(function(item) {
        return Object.assign({}, item, {
          changed_on: moment(item.changed_on)
        });
      });

    case UPDATE_AVATAR:
      return state.map(function(item) {
        item = Object.assign({}, item);
        if (item.changed_by && item.changed_by.id === action.userId) {
          item.changed_by = Object.assign({}, item.changed_by, {
            'avatar_hash': action.avatarHash
          });
        }

        return Object.assign({}, item);
      });

    case UPDATE_USERNAME:
      return state.map(function(item) {
        item = Object.assign({}, item);
        if (item.changed_by && item.changed_by.id === action.userId) {
          item.changed_by = Object.assign({}, item.changed_by, {
            'username': action.username,
            'slug': action.slug
          });
        }

        return Object.assign({}, item);
      });

    default:
      return state;
  }
}