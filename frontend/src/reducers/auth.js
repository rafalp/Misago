export default function auth(state={}, action=null) {
  if (action.type == 'NOT_YET') {
    return {};
  } else {
    return state;
  }
}
