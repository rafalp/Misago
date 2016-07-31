import React from 'react';
import PostsList from 'misago/components/posts-list'; // jshint ignore:line
import Header from './header'; // jshint ignore:line
import Paginator from './paginator'; // jshint ignore:line
import ToolbarTop from './toolbar-top'; // jshint ignore:line
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';
import * as posts from 'misago/reducers/posts';
import store from 'misago/services/store';
import * as thread from 'misago/reducers/thread';
import title from 'misago/services/page-title';

export default class extends React.Component {
  componentDidMount() {
    if (this.shouldFetchData()) {
      this.fetchData();
      this.setPageTitle();
    }
  }

  componentDidUpdate() {
    if (this.shouldFetchData()) {
      this.fetchData();
      this.setPageTitle();
    }
  }

  shouldFetchData() {
    if (this.props.posts.isLoaded) {
      const page = (this.props.params.page || 1) * 1;
      return page != this.props.posts.page;
    } else {
      return false;
    }
  }

  fetchData() {
    store.dispatch(posts.unload());

    ajax.get(this.props.thread.api.posts, {
      page: this.props.params.page || 1
    }, 'posts').then((data) => {
      store.dispatch(thread.replace(data));
      store.dispatch(posts.load(data.post_set));
    }, (rejection) => {
      snackbar.apiError(rejection);
    });
  }

  setPageTitle() {
    title.set({
      title: this.props.thread.title,
      page: (this.props.params.page || 1) * 1
    });
  }

  render() {
    /* jshint ignore:start */
    return <div className="page page-thread">
      <Header {...this.props} />
      <div className="container">

        <ToolbarTop {...this.props} />
        <PostsList {...this.props} />
        <Paginator {...this.props} />

      </div>
    </div>;
    /* jshint ignore:end */
  }
}