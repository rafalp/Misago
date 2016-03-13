import React from 'react';
import UserCard from 'misago/components/users-list/user-card' // jshint ignore:line
import UserPreview from 'misago/components/users-list/user-preview' // jshint ignore:line
import batch from 'misago/utils/batch'; // jshint ignore:line

export default class extends React.Component {
  getPager() {
    if (this.props.pages > 1) {
      /* jshint ignore:start */
      return <Pager {...this.props} />
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getClassName() {
    if (this.props.className) {
      return "users-cards-list " + this.props.className + " ui-ready";
    } else {
      return "users-cards-list ui-ready";
    }
  }

  getColClassName() {
    return "col-md-" + (12 / this.props.cols);
  }

  getBody() {
    if (this.props.isLoaded) {
      /* jshint ignore:start */
      return batch(this.props.users, this.props.cols).map((row, r) => {
        return <div className="row" key={r}>
          {row.map((user) => {
            return <div className={this.getColClassName()} key={user.id}>
              <UserCard user={user}
                        showStatus={this.props.showStatus}
                        showRank={this.props.showRank} />
            </div>;
          })}
        </div>;
      });
      /* jshint ignore:end */
    } else {
      /* jshint ignore:start */
      let row = [];
      for (let i = 0; i < this.props.cols; i ++) {
        if (i === 0) {
          row.push(this.getColClassName());
        } else {
          row.push(this.getColClassName() + ' hidden-xs hidden-sm');
        }
      }

      return <div className="row">
        {row.map((className, i) => {
          return <div className={className} key={i}>
            <UserPreview showStatus={this.props.showStatus} />
          </div>;
        })}
      </div>;
      /* jshint ignore:end */
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className="users-cards-list ui-ready">
      {this.getBody()}
    </div>;
    /* jshint ignore:end */
  }
}