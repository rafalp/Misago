import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line
import Li from 'misago/components/li'; //jshint ignore:line
import FollowButton from 'misago/components/profile/follow-button'; // jshint ignore:line
import misago from 'misago/index'; //jshint ignore:line

export class SideNav extends React.Component {
  render() {
    // jshint ignore:start
    return <div className="list-group nav-side">
      {this.props.pages.map((page) => {
        return <Link to={this.props.baseUrl + page.component + '/'}
                     className="list-group-item"
                     activeClassName="active"
                     key={page.component}>
          <span className="material-icon">
            {page.icon}
          </span>
          {page.name}
        </Link>;
      })}
    </div>;
    // jshint ignore:end
  }
}

export class CompactNav extends SideNav {
  showSpecialOptions() {
    return this.props.profile.acl.can_follow || this.props.profile.acl.can_moderate;
  }

  getFollowButton() {
    if (this.props.profile.acl.can_follow) {
      /* jshint ignore:start */
      return <FollowButton className="btn btn-block"
                           profile={this.props.profile} />;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getModerationButton() {
    if (this.props.profile.acl.can_moderate) {
      /* jshint ignore:start */
      return <button type="button" className="btn btn-default btn-block"
                     onClick={this.props.toggleModeration}>
        <span className="material-icon">
          tonality
        </span>
        {gettext("Moderation")}
      </button>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getSpecialOptions() {
    if (this.showSpecialOptions()) {
      /* jshint ignore:start */
      return <li className="dropdown-buttons">
        {this.getFollowButton()}
        {this.getModerationButton()}
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    // jshint ignore:start
    return <ul className="dropdown-menu" role="menu">
      {this.getSpecialOptions()}
      {this.showSpecialOptions() ? <li className="divider" /> : null}
      {this.props.pages.map((page) => {
        return <Li path={this.props.baseUrl + page.component + '/'}
                   key={page.component}>
          <Link to={this.props.baseUrl + page.component + '/'}
                onClick={this.props.hideNav}>
            <span className="material-icon">
              {page.icon}
            </span>
            {page.name}
          </Link>
        </Li>;
      })}
    </ul>;
    // jshint ignore:end
  }
}