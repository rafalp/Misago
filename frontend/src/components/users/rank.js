import React from 'react';
import title from 'misago/services/page-title';

export default class extends React.Component {
  componentDidMount() {
    title.set({
      title: this.props.route.rank.name,
      parent: gettext("Users")
    });
  }

  render() {
    /* jshint ignore:start */
    return <div>
      <div className="container">
       Hello, this is users with rank list!
      </div>
    </div>;
    /* jshint ignore:end */
  }
}