import React from 'react';
import List from 'misago/components/users/rank/list' // jshint ignore:line
import ListLoading from 'misago/components/users/rank/list-loading' // jshint ignore:line
import misago from 'misago/index';
import { dehydrate } from 'misago/reducers/users';
import polls from 'misago/services/polls';
import store from 'misago/services/store';
import title from 'misago/services/page-title';

export default class extends React.Component {
  constructor(props) {
    super(props);

    if (misago.has('USERS')) {
      this.initWithPreloadedData(misago.pop('USERS'));
    } else {
      this.initWithoutPreloadedData();
    }

    this.startPolling(props.params.page || 1);
  }

  initWithPreloadedData(data) {
    this.state = Object.assign(data, {
      isLoaded: true
    });
    store.dispatch(dehydrate(data.results));
  }

  initWithoutPreloadedData() {
    this.state = {
      isLoaded: false
    };
  }

  startPolling(page) {
    polls.start({
      poll: 'rank-users',
      url: misago.get('USERS_API'),
      data: {
        rank: this.props.route.rank.id,
        page: page
      },
      frequency: 90 * 1000,
      update: this.update
    });
  }

  /* jshint ignore:start */
  update = (data) => {
    store.dispatch(dehydrate(data.results));

    data.isLoaded = true;
    this.setState(data);
  };
  /* jshint ignore:end */

  componentDidMount() {
    title.set({
      title: this.props.route.rank.name,
      page: this.props.params.page || null,
      parent: gettext("Users")
    });
  }

  componentWillUnmount() {
    polls.stop('rank-users');
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.params.page !== nextProps.params.page) {
      title.set({
        title: this.props.route.rank.name,
        page: nextProps.params.page || null,
        parent: gettext("Users")
      });

      this.setState({
        isLoaded: false
      });

      polls.stop('rank-users');
      this.startPolling(nextProps.params.page);
    }
  }

  getClassName() {
    if (this.props.route.rank.css_class) {
      return 'rank-users-list rank-users-' + this.props.route.rank.css_class;
    } else {
      return 'rank-users-list';
    }
  }

  getRankDescription() {
    if (this.props.route.rank.description) {
      /* jshint ignore:start */
      return <div className="rank-description">
        <div className="lead" dangerouslySetInnerHTML={{
          __html: this.props.route.rank.description.html
        }} />
      </div>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getComponent() {
    if (this.state.isLoaded) {
      if (this.state.count > 0) {
        /* jshint ignore:start */
        let baseUrl = misago.get('USERS_LIST_URL') + this.props.route.rank.slug + '/';
        return <List baseUrl={baseUrl}
                     users={this.props.users}
                     {...this.state} />;
        /* jshint ignore:end */
      } else {
        /* jshint ignore:start */
        return <p className="lead">
          {gettext("There are no users with this rank at the moment.")}
        </p>;
        /* jshint ignore:end */
      }
    } else {
      /* jshint ignore:start */
      return <ListLoading />;
      /* jshint ignore:end */
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getClassName()}>
      <div className="container">
        {this.getRankDescription()}
        {this.getComponent()}
      </div>
    </div>;
    /* jshint ignore:end */
  }
}