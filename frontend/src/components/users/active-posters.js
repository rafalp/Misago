import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import Status, { StatusIcon, StatusLabel } from 'misago/components/user-status'; // jshint ignore:line
import misago from 'misago/index';
import { dehydrate } from 'misago/reducers/users';
import polls from 'misago/services/polls';
import store from 'misago/services/store';
import title from 'misago/services/page-title';
import * as random from 'misago/utils/random'; // jshint ignore:line

export class ActivePoster extends React.Component {
  getClassName() {
    if (this.props.rank.css_class) {
      return "list-group-item list-group-rank-" + this.props.rank.css_class;
    } else {
      return "list-group-item";
    }
  }

  getUserStatus() {
    if (this.props.user.status) {
      /* jshint ignore:start */
      return <Status user={this.props.user} status={this.props.user.status}>
        <StatusIcon user={this.props.user}
                    status={this.props.user.status} />
        <StatusLabel user={this.props.user}
                     status={this.props.user.status}
                     className="status-label hidden-xs hidden-sm" />
      </Status>;
      /* jshint ignore:end */
    } else {
      /* jshint ignore:start */
      return <span className="user-status">
        <span className="status-icon ui-preview">
          &nbsp;
        </span>
        <span className="status-label ui-preview hidden-xs hidden-sm">
          &nbsp;
        </span>
      </span>;
      /* jshint ignore:end */
    }
  }

  getRankName() {
    if (this.props.rank.is_tab) {
      /* jshint ignore:start */
      let rankUrl = misago.get('USERS_LIST_URL') + this.props.rank.slug + '/';
      return <Link to={rankUrl} className="rank-name">
        {this.props.rank.name}
      </Link>;
      /* jshint ignore:end */
    } else {
      /* jshint ignore:start */
      return <span className="rank-name">
        {this.props.rank.name}
      </span>;
      /* jshint ignore:end */
    }
  }

  getUserTitle() {
    if (this.props.user.title) {
      /* jshint ignore:start */
      return <span className="user-title hidden-xs hidden-sm">
        {this.props.user.title}
      </span>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <li className={this.getClassName()}>
      <div className="rank-user-avatar">
        <a href={this.props.user.absolute_url}>
          <Avatar user={this.props.user} size="50" />
        </a>
      </div>

      <div className="rank-user">
        <div className="user-name">
          <a href={this.props.user.absolute_url} className="item-title">
            {this.props.user.username}
          </a>
        </div>
        {this.getUserStatus()}
        {this.getRankName()}
        {this.getUserTitle()}
      </div>

      <div className="rank-position">
        <div className="stat-value">#{this.props.counter}</div>
        <div className="text-muted">{gettext("Rank")}</div>
      </div>

      <div className="rank-posts-counted">
        <div className="stat-value">{this.props.user.meta.score}</div>
        <div className="text-muted">{gettext("Ranked posts")}</div>
      </div>

      <div className="rank-posts-total">
        <div className="stat-value">{this.props.user.posts}</div>
        <div className="text-muted">{gettext("Total posts")}</div>
      </div>
    </li>;
    /* jshint ignore:end */
  }
}

export class ActivePosters extends React.Component {
  getLeadMessage() {
    let message = ngettext(
        "%(posters)s most active poster from last %(days)s days.",
        "%(posters)s most active posters from last %(days)s days.",
        this.props.count);

    return interpolate(message, {
      posters: this.props.count,
      days: this.props.trackedPeriod
    }, true);
  }

  render() {
    /* jshint ignore:start */
    return <div className="active-posters-list">
      <div className="container">
        <p className="lead">
          {this.getLeadMessage()}
        </p>

        <div className="active-posters ui-ready">
          <ul className="list-group">
            {this.props.users.map((user, i) => {
              return <ActivePoster user={user}
                                   rank={user.rank}
                                   counter={i + 1}
                                   key={user.id} />;
            })}
          </ul>
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}

export class ActivePostersLoading extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="active-posters-list">
      <div className="container">
        <p className="lead ui-preview-paragraph">
          {random.range(3, 4).map((i) => {
            return <span key={i} className="ui-preview-text" style={{width: random.int(50, 120) + "px"}}>&nbsp;</span>
          })}
        </p>

        <div className="active-posters ui-preview">
          <ul className="list-group">
            {random.range(5, 10).map((i, counter) => {
              return <li key={i} className="list-group-item">
                <div className="rank-user-avatar">
                  <span>
                    <Avatar size="50" />
                  </span>
                </div>

                <div className="rank-user">
                  <div className="user-name">
                    <span className="item-title">
                      <span className="ui-preview-text" style={{width: random.int(30, 80) + "px"}}>&nbsp;</span>
                    </span>
                  </div>

                  <span className="user-status">
                    <span className="status-icon ui-preview">
                      &nbsp;
                    </span>
                    <span className="status-label ui-preview hidden-xs hidden-sm">
                      &nbsp;
                    </span>
                  </span>
                  <span className="rank-name">
                    <span className="ui-preview-text" style={{width: random.int(30, 50) + "px"}}>&nbsp;</span>
                  </span>
                  <span className="user-title hidden-xs hidden-sm">
                    <span className="ui-preview-text" style={{width: random.int(30, 50) + "px"}}>&nbsp;</span>
                  </span>
                </div>

                <div className="rank-position">
                  <div className="stat-value">
                    <span className="ui-preview-text" style={{width: "30px"}}>&nbsp;</span>
                  </div>
                  <div className="text-muted">{gettext("Rank")}</div>
                </div>

                <div className="rank-posts-counted">
                  <div className="stat-value">
                    <span className="ui-preview-text" style={{width: "30px"}}>&nbsp;</span>
                  </div>
                  <div className="text-muted">{gettext("Ranked posts")}</div>
                </div>

                <div className="rank-posts-total">
                  <div className="stat-value">
                    <span className="ui-preview-text" style={{width: "30px"}}>&nbsp;</span>
                  </div>
                  <div className="text-muted">{gettext("Total posts")}</div>
                </div>
              </li>;
            })}
          </ul>
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}

export class NoActivePosters extends React.Component {
  getEmptyMessage() {
    return interpolate(
      gettext("No users have posted any new messages during last %(days)s days."),
      {'days': this.props.trackedPeriod}, true);
  }

  render() {
    /* jshint ignore:start */
    return <div className="active-posters-list">
      <div className="container">
        <p className="lead">
          {this.getEmptyMessage()}
        </p>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}

export default class extends React.Component {
  constructor(props) {
    super(props);

    if (misago.has('USERS')) {
      this.initWithPreloadedData(misago.pop('USERS'));
    } else {
      this.initWithoutPreloadedData();
    }

    this.startPolling();
  }

  initWithPreloadedData(data) {
    this.state = {
      isLoaded: true,

      trackedPeriod: data.tracked_period,
      count: data.count
    };

    store.dispatch(dehydrate(data.results));
  }

  initWithoutPreloadedData() {
    this.state = {
      isLoaded: false
    };
  }

  startPolling() {
    polls.start({
      poll: 'active-posters',
      url: misago.get('USERS_API'),
      data: {
        list: 'active'
      },
      frequency: 90 * 1000,
      update: this.update
    });
  }

  /* jshint ignore:start */
  update = (data) => {
    this.setState({
      isLoaded: true,

      trackedPeriod: data.tracked_period,
      count: data.count
    });

    store.dispatch(dehydrate(data.results));
  };
  /* jshint ignore:end */

  componentDidMount() {
    title.set({
      title: this.props.route.extra.name,
      parent: gettext("Users")
    });
  }

  componentWillUnmount() {
    polls.stop('active-posters');
  }

  render() {
    if (this.state.isLoaded) {
      if (this.state.count > 0) {
        /* jshint ignore:start */
        return <ActivePosters users={this.props.users}
                              trackedPeriod={this.state.trackedPeriod}
                              count={this.state.count} />;
        /* jshint ignore:end */
      } else {
        /* jshint ignore:start */
        return <NoActivePosters trackedPeriod={this.state.trackedPeriod} />;
        /* jshint ignore:end */
      }
    } else {
      /* jshint ignore:start */
      return <ActivePostersLoading />;
      /* jshint ignore:end */
    }
  }
}