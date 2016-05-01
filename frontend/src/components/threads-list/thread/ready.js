import React from 'react';
import Loader from 'misago/components/loader'; // jshint ignore:line
import DetailsCompact from 'misago/components/threads-list/thread/details/compact'; // jshint ignore:line
import DetailsFull from 'misago/components/threads-list/thread/details/full'; // jshint ignore:line
import Flags from 'misago/components/threads-list/thread/flags'; // jshint ignore:line
import Icon from 'misago/components/threads-list/thread/icon'; // jshint ignore:line
import ThreadOptions from 'misago/components/threads-list/thread/options'; // jshint ignore:line

export default class extends React.Component {
  getIcon() {
    if (this.props.isBusy) {
      /* jshint ignore:start */
      return <Loader />;
      /* jshint ignore:end */
    } else {
      /* jshint ignore:start */
      return <Icon thread={this.props.thread} />;
      /* jshint ignore:end */
    }
  }

  getOptions() {
    if (this.props.showOptions) {
      /* jshint ignore:start */
      return <ThreadOptions thread={this.props.thread}
                            disabled={this.props.isBusy}
                            isSelected={this.props.isSelected} />;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getClassName() {
    let styles = ['list-group-item'];

    if (this.props.thread.is_read) {
      styles.push('thread-read');
    } else {
      styles.push('thread-new');
    }

    if (this.props.isBusy) {
      styles.push('thread-busy');
    } else if (this.props.isSelected) {
      styles.push('thread-selected');
    }

    if (this.props.showOptions) {
      if (this.props.thread.moderation.length) {
        styles.push('thread-ops-two');
      } else {
        styles.push('thread-ops-one');
      }
    }

    return styles.join(' ');
  }

  render () {
    /* jshint ignore:start */
    return <li className={this.getClassName()}>

      <div className="thread-icon">
        {this.getIcon()}
        <Flags thread={this.props.thread} />
      </div>

      {this.getOptions()}

      <div className="thread-main">

        <a href={this.props.thread.absolute_url} className="item-title thread-title">
          {this.props.thread.title}
        </a>

        <DetailsFull categories={this.props.categories}
                     list={this.props.list}
                     thread={this.props.thread} />

        <DetailsCompact categories={this.props.categories}
                        list={this.props.list}
                        thread={this.props.thread} />

      </div>

      <div className="clearfix" />
    </li>;
    /* jshint ignore:end */
  }
}