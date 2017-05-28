import moment from 'moment';
import * as post from 'misago/reducers/post';
import * as posts from 'misago/reducers/posts';
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';

export function approve(props) {
  props.selection.forEach((selection) => {
    store.dispatch(post.patch(selection, {
      is_unapproved: false
    }));

    const ops = [
      {'op': 'replace', 'path': 'is-unapproved', 'value': false}
    ];

    const previousState = {
      is_unapproved: selection.is_unapproved
    };

    patch(selection, ops, previousState);
  });

  store.dispatch(posts.deselectAll());
}

export function protect(props) {
  props.selection.forEach((selection) => {
    store.dispatch(post.patch(selection, {
      is_protected: false
    }));

    const ops = [
      {'op': 'replace', 'path': 'is-protected', 'value': true}
    ];

    const previousState = {
      is_protected: selection.is_protected
    };

    patch(selection, ops, previousState);
  });

  store.dispatch(posts.deselectAll());
}

export function unprotect(props) {
  props.selection.forEach((selection) => {
    store.dispatch(post.patch(selection, {
      is_protected: false
    }));

    const ops = [
      {'op': 'replace', 'path': 'is-protected', 'value': false}
    ];

    const previousState = {
      is_protected: selection.is_protected
    };

    patch(selection, ops, previousState);
  });

  store.dispatch(posts.deselectAll());
}

export function hide(props) {
  props.selection.forEach((selection) => {
    store.dispatch(post.patch(selection, {
      is_hidden: true,
      hidden_on: moment(),
      hidden_by_name: props.user.username,
      url: Object.assign(selection.url, {
        hidden_by: props.user.url
      })
    }));

    const ops = [
      {'op': 'replace', 'path': 'is-hidden', 'value': true}
    ];

    const previousState = {
      is_hidden: selection.is_hidden,
      hidden_on: selection.hidden_on,
      hidden_by_name: selection.hidden_by_name,
      url: selection.url
    };

    patch(selection, ops, previousState);
  });

  store.dispatch(posts.deselectAll());
}

export function unhide(props) {
  props.selection.forEach((selection) => {
    store.dispatch(post.patch(selection, {
      is_hidden: false
    }));

    const ops = [
      {'op': 'replace', 'path': 'is-hidden', 'value': false}
    ];

    const previousState = {
      is_hidden: selection.is_hidden
    };

    patch(selection, ops, previousState);
  });

  store.dispatch(posts.deselectAll());
}

export function patch(selection, ops, previousState) {
  ajax.patch(selection.api.index, ops).then((newState) => {
    store.dispatch(post.patch(selection, newState));
  }, (rejection) => {
    if (rejection.status === 400) {
      snackbar.error(rejection.detail[0]);
    } else {
      snackbar.apiError(rejection);
    }

    store.dispatch(post.patch(selection, previousState));
  });
}

export function merge(props) {
  let confirmed = confirm(gettext("Are you sure you want to merge selected posts? This action is not reversible!"));
  if (!confirmed) {
    return;
  }

  props.selection.slice(1).map((selection) => {
    store.dispatch(post.patch(selection, {
      isDeleted: true
    }));
  });

  ajax.post(props.thread.api.posts.merge, {
    posts: props.selection.map((post) => post.id)
  }).then((data) => {
    store.dispatch(post.patch(data, post.hydrate(data)));
  }, (rejection) => {
    if (rejection.status === 400) {
      snackbar.error(rejection.detail);
    } else {
      snackbar.apiError(rejection);
    }

    props.selection.slice(1).map((selection) => {
      store.dispatch(post.patch(selection, {
        isDeleted: false
      }));
    });
  });

  store.dispatch(posts.deselectAll());
}

export function remove(props) {
  let confirmed = confirm(gettext("Are you sure you want to delete selected posts? This action is not reversible!"));
  if (!confirmed) {
    return;
  }

  props.selection.forEach((selection) => {
    store.dispatch(post.patch(selection, {
      isDeleted: true
    }));

    ajax.delete(selection.api.index).then(() => {
      return;
    }, (rejection) => {
      if (rejection.status === 400) {
        snackbar.error(rejection.detail);
      } else {
        snackbar.apiError(rejection);
      }

      store.dispatch(post.patch(selection, {
        isDeleted: false
      }));
    });
  });

  store.dispatch(posts.deselectAll());
}