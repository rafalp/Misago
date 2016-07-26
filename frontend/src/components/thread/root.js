import { connect } from 'react-redux';
import Route from 'misago/components/thread/route';
import misago from 'misago/index';

export function select(store) {
  return {
    'posts': store.posts,
    'thread': store.thread,
    'tick': store.tick.tick,
    'user': store.auth.user
  };
}

export function paths() {
  return [
    {
      path: misago.get('THREAD').url.index,
      component: connect(select)(Route)
    },
    {
      path: misago.get('THREAD').url.index + ':page/',
      component: connect(select)(Route)
    }
  ];
}