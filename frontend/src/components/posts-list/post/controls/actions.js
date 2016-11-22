import moment from 'moment';
import * as post from 'misago/reducers/post';
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';

export function approve(props) {
  store.dispatch(post.patch(props.post, {
    is_unapproved: false
  }));

  const ops = [
    {'op': 'replace', 'path': 'is-unapproved', 'value': false}
  ];

  const previousState = {
    is_unapproved: props.post.is_unapproved
  };

  patch(props, ops, previousState);
}

export function protect(props) {
  store.dispatch(post.patch(props.post, {
    is_protected: true
  }));

  const ops = [
    {'op': 'replace', 'path': 'is-protected', 'value': true}
  ];

  const previousState = {
    is_protected: props.post.is_protected
  };

  patch(props, ops, previousState);
}

export function unprotect(props) {
  store.dispatch(post.patch(props.post, {
    is_protected: false
  }));

  const ops = [
    {'op': 'replace', 'path': 'is-protected', 'value': false}
  ];

  const previousState = {
    is_protected: props.post.is_protected
  };

  patch(props, ops, previousState);
}

export function hide(props) {
  store.dispatch(post.patch(props.post, {
    is_hidden: true,
    hidden_on: moment(),
    hidden_by_name: props.user.username,
    url: Object.assign(props.post.url, {
      hidden_by: props.user.absolute_url
    })
  }));

  const ops = [
    {'op': 'replace', 'path': 'is-hidden', 'value': true}
  ];

  const previousState = {
    is_hidden: props.post.is_hidden,
    hidden_on: props.post.hidden_on,
    hidden_by_name: props.post.hidden_by_name,
    url: props.post.url
  };

  patch(props, ops, previousState);
}

export function unhide(props) {
  store.dispatch(post.patch(props.post, {
    is_hidden: false
  }));

  const ops = [
    {'op': 'replace', 'path': 'is-hidden', 'value': false}
  ];

  const previousState = {
    is_hidden: props.post.is_hidden
  };

  patch(props, ops, previousState);
}

export function like(props) {
  store.dispatch(post.patch(props.post, {
    is_liked: true,
    likes: props.post.likes + 1,
    last_likes: [props.user].concat(props.post.last_likes.slice(0, -1))
  }));

  const ops = [
    {'op': 'replace', 'path': 'is-liked', 'value': true}
  ];

  const previousState = {
    is_liked: props.post.is_liked,
    likes: props.post.likes,
    last_likes: props.post.last_likes
  };

  patch(props, ops, previousState);
}

export function unlike(props) {
  store.dispatch(post.patch(props.post, {
    is_liked: false,
    likes: props.post.likes - 1
  }));

  const ops = [
    {'op': 'replace', 'path': 'is-liked', 'value': false}
  ];

  const previousState = {
    is_liked: props.post.is_liked,
    likes: props.post.likes,
    last_likes: props.post.last_likes
  };

  patch(props, ops, previousState);
}

export function patch(props, ops, previousState) {
  ajax.patch(props.post.api.index, ops).then((newState) => {
    store.dispatch(post.patch(props.post, newState));
  }, (rejection) => {
    if (rejection.status === 400) {
      snackbar.error(rejection.detail[0]);
    } else {
      snackbar.apiError(rejection);
    }

    store.dispatch(post.patch(props.post, previousState));
  });
}

export function remove(props) {
  let confirmed = confirm(gettext("Are you sure you want to delete this post? This action is not reversible!"));
  if (!confirmed) {
    return;
  }

  store.dispatch(post.patch(props.post, {
    isDeleted: true
  }));

  ajax.delete(props.post.api.index).then(() => {
    snackbar.success(gettext("Post has been deleted."));
  }, (rejection) => {
    if (rejection.status === 400) {
      snackbar.error(rejection.detail);
    } else {
      snackbar.apiError(rejection);
    }

    store.dispatch(post.patch(props.post, {
      isDeleted: false
    }));
  });
}