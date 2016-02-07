import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import Status, { StatusIcon, StatusLabel } from 'misago/components/user-status'; // jshint ignore:line
import misago from 'misago/index';
import { dehydrate } from 'misago/reducers/users';
import polls from 'misago/services/polls';
import store from 'misago/services/store';
import title from 'misago/services/page-title';
import batch from 'misago/utils/batch'; // jshint ignore:line
import * as random from 'misago/utils/random'; // jshint ignore:line
import resetScroll from 'misago/utils/reset-scroll'; // jshint ignore:line

export class RankUserCard extends React.Component {
  getClassName() {
    if (this.props.user.rank.css_class) {
      return 'user-card user-card-' + this.props.user.rank.css_class;
    } else {
      return 'user-card';
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
                     className="status-label" />
      </Status>;
      /* jshint ignore:end */
    } else {
      /* jshint ignore:start */
      return <span className="user-status">
        <span className="status-icon ui-preview">
          &nbsp;
        </span>
        <span className="status-label ui-preview">
          &nbsp;
        </span>
      </span>;
      /* jshint ignore:end */
    }
  }

  getUserTitle() {
    if (this.props.user.title) {
      /* jshint ignore:start */
      return <span className="user-title">{this.props.user.title}</span>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getUserJoinedOn() {
    /* jshint ignore:start */
    let title = interpolate(gettext("Member since %(joined_on)s"), {
      'joined_on': this.props.user.joined_on.format('LL, LT')
    }, true);

    return <span className="user-joined-on" title={title}>
      {this.props.user.joined_on.fromNow()}
    </span>;
    /* jshint ignore:end */
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getClassName()}>
      <div className="user-card-bg-image">
        <Avatar user={this.props.user} size="400" className="bg-image" />

        <div className="user-card-bg">
          <div className="user-details">

            <div className="user-avatar">
              <a href={this.props.user.absolute_url}>
                <Avatar user={this.props.user} size="400" />
              </a>
            </div>

            <h4 className="user-name">
              <a href={this.props.user.absolute_url} className="item-title">
                {this.props.user.username}
              </a>
            </h4>

            <p className="user-subscript">
              {this.getUserStatus()}
              {this.getUserTitle()}
              {this.getUserJoinedOn()}
            </p>

          </div>
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}

export class RankUsersPager extends React.Component {
  getPreviousPage() {
    if (this.props.previous || this.props.first) {
      /* jshint ignore:start */
      let url = this.props.baseUrl;
      if (this.props.previous) {
        url += this.props.previous + '/';
      }

      return <li className="previous">
        <Link to={url} onClick={resetScroll}>
          <span aria-hidden="true" className="material-icon">
            arrow_back
          </span>
        </Link>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getNextPage() {
    if (this.props.next) {
      /* jshint ignore:start */
      let url = this.props.baseUrl + this.props.next + '/';
      return <li className="next">
        <Link to={url} onClick={resetScroll}>
          <span aria-hidden="true" className="material-icon">
            arrow_forward
          </span>
        </Link>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getProgessBar() {
    /* jshint ignore:start */
    return <ul className="pager-progress-bar">
      {this.props.page_range.map((page) => {
        let className = page === this.props.page ? 'active' : null;
        let url = this.props.baseUrl;

        if (page > 1) {
          url += page + '/';
        }

        return <li key={page} className={className}>
          <Link to={url} onClick={resetScroll}>
            {page}
          </Link>
        </li>;
      })}
    </ul>;
    /* jshint ignore:end */
  }

  render() {
    /* jshint ignore:start */
    return <div className="pager-undercontent">
      <nav>
        <ul className="pager">
          {this.getPreviousPage()}
          {this.getNextPage()}
        </ul>
        {this.getProgessBar()}
      </nav>
    </div>;
    /* jshint ignore:end */
  }
}

export class RankUsers extends React.Component {
  getPager() {
    if (this.props.pages > 1) {
      /* jshint ignore:start */
      return <RankUsersPager {...this.props} />
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <div>
      <div className="users-cards-list ui-ready">
        {batch(this.props.users, 4).map((row, r) => {
          return <div className="row" key={r}>
            {row.map((user) => {
              return <div className="col-md-3" key={user.id}>
                <RankUserCard user={user} />
              </div>;
            })}
          </div>;
        })}
      </div>
      {this.getPager()}
    </div>;
    /* jshint ignore:end */
  }
}

export class RankUsersLoading extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div>
      <div className="users-cards-list ui-ready">
        <div className="row">
          {[0, 1, 2, 3].map((i) => {
            return <div className="col-md-3" key={i}>
              <div className='user-card ui-preview'>
                <div className="user-card-bg-image">
                  <Avatar size="400" className="bg-image" />

                  <div className="user-card-bg">
                    <div className="user-details">

                      <div className="user-avatar">
                        <Avatar size="400" />
                      </div>

                      <h4 className="user-name">
                        <span className="item-title">
                          <span className="ui-preview-text" style={{width: random.int(60, 150) + "px"}}>&nbsp;</span>
                        </span>
                      </h4>

                      <p className="user-subscript">

                        <span className="user-status">
                          <span className="status-icon ui-preview">
                            &nbsp;
                          </span>
                          <span className="status-label ui-preview">
                            &nbsp;
                          </span>
                        </span>
                        <span className="user-joined-on">
                          <span className="ui-preview-text" style={{width: random.int(30, 50) + "px"}}>&nbsp;</span>
                        </span>

                      </p>

                    </div>
                  </div>
                </div>
              </div>
            </div>;
          })}
        </div>
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
        list: 'rank',
        rank: this.props.route.rank.slug,
        page: page
      },
      frequency: 90 * 1000,
      update: this.update
    });
  }

  /* jshint ignore:start */
  update = (data) => {
    data.isLoaded = true;
    this.setState(data);

    store.dispatch(dehydrate(data.results));
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
        return <RankUsers baseUrl={baseUrl}
                          rank={this.props.route.rank}
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
      return <RankUsersLoading />;
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