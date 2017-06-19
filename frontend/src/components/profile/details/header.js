/* jshint ignore:start */
import React from 'react';

export default function({ onEdit, showEditButton }) {
  return (
    <div>
      <nav className="toolbar">
        <div className="row">
          <div className="col-sm-8 col-md-10">
            <h3 className="md-margin-top-no">
              {gettext("Profile details")}
            </h3>
          </div>
          <EditButton
            onEdit={onEdit}
            showEditButton={showEditButton}
          />
        </div>
      </nav>
    </div>
  );
}

export function EditButton({ onEdit, showEditButton }) {
  if (!showEditButton) return null;

  return (
    <div className="col-sm-4 col-md-2">
      <button
        className="btn btn-default btn-outline btn-block"
        onClick={onEdit}
        type="button"
      >
        {gettext("Edit")}
      </button>
    </div>
  );
}