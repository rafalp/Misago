import React from 'react';
import Button from 'misago/components/button'; // jshint ignore:line
import Search from 'misago/components/search'; // jshint ignore:line
import UsersList from 'misago/components/users-list/root'; // jshint ignore:line
import misago from 'misago/index';
import { dehydrate, append } from 'misago/reducers/users'; // jshint ignore:line
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';
import title from 'misago/services/page-title';

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.setSpecialProps();

    if (misago.has(this.PRELOADED_DATA_KEY)) {
      this.initWithPreloadedData(misago.pop(this.PRELOADED_DATA_KEY));
    } else {
      this.initWithoutPreloadedData();
    }
  }

  setSpecialProps() {
    this.PRELOADED_DATA_KEY = 'PROFILE_FOLLOWERS';
    this.TITLE = gettext('Followers');
    this.API_FILTER = 'followers';
  }

  initWithPreloadedData(data) {
    this.state = {
      isLoaded: true,
      isBusy: false,

      search: '',

      count: data.count,
      more: data.more,

      page: data.page,
      pages: data.pages
    };

    store.dispatch(dehydrate(data.results));
  }

  initWithoutPreloadedData() {
    this.state = {
      isLoaded: false,
      isBusy: false,

      search: '',

      count: 0,
      more: 0,

      page: 1,
      pages: 1
    };

    this.loadUsers();
  }

  loadUsers(page=1, search=null) {
    ajax.get(misago.get('USERS_API'), {
      [this.API_FILTER]: this.props.profile.id,
      name: search,
      page: page || 1
    }, 'user-' + this.API_FILTER).then((data) => {
      if (page === 1) {
        store.dispatch(dehydrate(data.results));
      } else {
        store.dispatch(append(data.results));
      }

      this.setState({
        isLoaded: true,
        isBusy: false,

        count: data.count,
        more: data.more,

        page: data.page,
        pages: data.pages
      });
    }, (rejection) => {
      snackbar.apiError(rejection);
    });
  }

  componentDidMount() {
    title.set({
      title: this.TITLE,
      parent: this.props.profile.username
    });
  }

  /* jshint ignore:start */
  loadMore = () => {
    this.setState({
      isBusy: true
    });

    this.loadUsers(this.state.page + 1, this.state.search);
  };

  search = (ev) => {
    this.setState({
      isLoaded: false,
      isBusy: true,

      search: ev.target.value,

      count: 0,
      more: 0,

      page: 1,
      pages: 1
    });

    this.loadUsers(1, ev.target.value);
  };
  /* jshint ignore:end */

  getLabel() {
    if (!this.state.isLoaded) {
      return gettext('Loading...');
    } else if (this.state.search) {
      let message = ngettext(
        "Found %(users)s user.",
        "Found %(users)s users.",
        this.state.count);

      return interpolate(message, {
        'users': this.state.count
      }, true);
    } else if (this.props.profile.id === this.props.user.id) {
      let message = ngettext(
        "You have %(users)s follower.",
        "You have %(users)s followers.",
        this.state.count);

      return interpolate(message, {
        'users': this.state.count
      }, true);
    } else {
      let message = ngettext(
        "%(username)s has %(users)s follower.",
        "%(username)s has %(users)s followers.",
        this.state.count);

      return interpolate(message, {
        'username': this.props.profile.username,
        'users': this.state.count
      }, true);
    }
  }

  getEmptyMessage() {
    if (this.state.search) {
      return gettext("Search returned no users matching specified criteria.");
    } else if (this.props.user.id === this.props.profile.id) {
      return gettext("You have no followers.");
    } else {
      return interpolate(gettext("%(username)s has no followers."), {
        'username': this.props.profile.username
      }, true);
    }
  }

  getMoreButton() {
    if (this.state.more) {
      /* jshint ignore:start */
      return <div className="pager-more">
        <Button loading={this.state.isBusy}
                onClick={this.loadMore}>
          {interpolate(gettext("Show more (%(more)s)"), {
            'more': this.state.more
          }, true)}
        </Button>
      </div>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getListBody() {
    if (this.state.isLoaded && this.state.count === 0) {
      /* jshint ignore:start */
      return <p className="lead">
        {this.getEmptyMessage()}
      </p>;
      /* jshint ignore:end */
    } else {
      /* jshint ignore:start */
      return <div>
        <UsersList isLoaded={this.state.isLoaded}
                   users={this.props.users}
                   showRank={true}
                   cols={2} />

        {this.getMoreButton()}
      </div>;
      /* jshint ignore:end */
    }
  }

  getClassName() {
    return 'profile-' + this.API_FILTER;
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getClassName()}>

      <nav className="toolbar">
        <h3 className="toolbar-left">
          {this.getLabel()}
        </h3>

        <Search className="toolbar-right"
                value={this.state.search}
                onChange={this.search}
                placeholder={gettext("Search history...")} />
      </nav>

      {this.getListBody()}

    </div>;
    /* jshint ignore:end */
  }
}