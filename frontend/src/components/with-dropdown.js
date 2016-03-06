import React from 'react';

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      dropdown: false
    };
  }

  /* jshint ignore:start */
  toggleNav = () => {
    this.setState({
      dropdown: !this.state.dropdown
    });
  };

  hideNav = () => {
    this.setState({
      dropdown: false
    });
  };
  /* jshint ignore:end */

  getCompactNavClassName() {
    if (this.state.dropdown) {
      return 'compact-nav open';
    } else {
      return 'compact-nav';
    }
  }
}