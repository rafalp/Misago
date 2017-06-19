/* jshint ignore:start */
import React from 'react';
import Select from 'misago/components/select';

export default class extends React.Component {
  onChange = (ev) => {
    const { field, onChange } = this.props;
    onChange(field.fieldname, ev.target.value);
  }

  render() {
    const { field, value } = this.props;
    const { input } = field;

    if (input.type === 'select') {
      return (
        <Select
          choices={input.choices}
          id={"id_" + field.fieldname}
          onChange={this.onChange}
          value={value}
        />
      );
    }

    if (input.type === 'textarea') {
      return (
        <textarea
          className="form-control"
          id={"id_" + field.fieldname}
          onChange={this.onChange}
          rows="4"
          type="text"
          value={value}
        />
      );
    }

    if (input.type === 'text') {
      return (
        <input
          className="form-control"
          id={"id_" + field.fieldname}
          onChange={this.onChange}
          type="text"
          value={value}
        />
      );
    }

    return null;
  }
}