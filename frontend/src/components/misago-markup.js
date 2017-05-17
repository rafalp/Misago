// jshint ignore:start
import React from 'react';
import onebox from 'misago/services/one-box';


export default class extends React.Component {
  componentDidMount() {
    onebox.render(this.documentNode);
  }

  componentDidUpdate(prevProps, prevState) {
    onebox.render(this.documentNode);
  }

  shouldComponentUpdate(nextProps, nextState) {
    return nextProps.markup !== this.props.markup;
  }

  render() {
    return (
      <article
        className="misago-markup"
        dangerouslySetInnerHTML={{__html: this.props.markup}}
        ref={(node) => { this.documentNode = node; }}
      />
    );
  }
}