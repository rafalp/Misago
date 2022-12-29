import React from "react"
import { Toolbar, ToolbarItem, ToolbarSection } from "../../Toolbar"

const ProfileDetailsHeader = ({ onEdit, showEditButton }) => (
  <Toolbar>
    <ToolbarSection auto>
      <ToolbarItem auto>
        <h3>{gettext("Details")}</h3>
      </ToolbarItem>
    </ToolbarSection>
    {showEditButton && (
      <ToolbarSection>
        <ToolbarItem>
          <button
            className="btn btn-default btn-outline btn-block"
            onClick={onEdit}
            type="button"
          >
            {gettext("Edit")}
          </button>
        </ToolbarItem>
      </ToolbarSection>
    )}
  </Toolbar>
)

export default ProfileDetailsHeader