/* jshint ignore:start */
import React from 'react';
import FieldInput from './field-input';
import FormGroup from 'misago/components/form-group';

export default function({ name, fields, onChange, value }) {
  return (
    <fieldset>
      <legend>{name}</legend>
      {fields.map((field) => {
        return (
          <FormGroup
            for={"id_" + field.fieldname}
            key={field.fieldname}
            label={field.label}
          >
            <FieldInput
              field={field}
              onChange={onChange}
              value={value[field.fieldname]}
            />
          </FormGroup>
        );
      })}
    </fieldset>
  );
}
