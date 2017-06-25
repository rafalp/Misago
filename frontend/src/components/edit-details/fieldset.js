/* jshint ignore:start */
import React from 'react';
import FieldInput from './field-input';
import FormGroup from 'misago/components/form-group';

export default function({ disabled, errors, fields, name, onChange, value }) {
  return (
    <fieldset>
      <legend>{name}</legend>
      {fields.map((field) => {
        return (
          <FormGroup
            for={"id_" + field.fieldname}
            key={field.fieldname}
            label={field.label}
            validation={errors[field.fieldname]}
          >
            <FieldInput
              disabled={disabled}
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
