import React from 'react';
import Button from 'misago/components/button'; // jshint ignore:line
import UsernameHistory from 'misago/components/username-history'; // jshint ignore:line
import misago from 'misago/index';
import { dehydrate, append } from 'misago/reducers/username-history'; // jshint ignore:line
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';
import title from 'misago/services/page-title';

export default class extends React.Component {
  constructor(props) {
    super(props);

    if (misago.has('PROFILE_NAME_HISTORY')) {
      this.initWithPreloadedData(misago.pop('PROFILE_NAME_HISTORY'));
    } else {
      this.initWithoutPreloadedData();
    }
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

    this.loadChanges();
  }

  loadChanges(page=1, search=null) {
    let searchState = search;

    ajax.get(misago.get('USERNAME_CHANGES_API'), {
      user: this.props.user.id,
      search: search,
      page: page || 1
    }).then((data) => {
      if (searchState !== null && searchState !== this.state.search) {
        return; // discard result
      }

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
      title: gettext("Username history"),
      parent: this.props.profile.username
    });
  }

  /* jshint ignore:start */
  loadMore = () => {
    this.setState({
      isBusy: true
    });

    this.loadChanges(this.state.page + 1, this.state.search);
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

    this.loadChanges(1, ev.target.value);
  };
  /* jshint ignore:end */

  getLabel() {
    if (this.state.isLoaded) {
      let message = ngettext(
        "Found %(changes)s username change.",
        "Found %(changes)s username changes.",
        this.state.count);

      return interpolate(message, {
        'changes': this.state.count
      }, true);
    } else {
      return gettext('Loading...');
    }
  }

  getEmptyMessage() {
    if (this.state.search) {
      return gettext("Search returned no username changes matching specified criteria.");
    } else if (this.props.user.id === this.props.profile.id) {
      return gettext("No name changes have been recorded for your account.");
    } else {
      return interpolate(gettext("%(username)s's username was never changed."), {
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
          {interpolate(gettext("Show older (%(more)s)"), {
            'more': this.state.more
          }, true)}
        </Button>
      </div>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className="profile-username-history">

      <nav className="toolbar">
        <p className="toolbar-left">
          {this.getLabel()}
        </p>

        <input type="text"
               className="form-control toolbar-right"
               value={this.state.search}
               onChange={this.search}
               placeholder={gettext("Search history...")} />
      </nav>

      <UsernameHistory isLoaded={this.state.isLoaded}
                       emptyMessage={this.getEmptyMessage()}
                       changes={this.props['username-history']} />

      {this.getMoreButton()}

    </div>;
    /* jshint ignore:end */
  }
}