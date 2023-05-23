import React from "react"
import { Toolbar, ToolbarItem, ToolbarSection, ToolbarSpacer } from "../Toolbar"

const ThreadToolbarThird = () => (
  <Toolbar className="thread-toolbar-third">
    <ToolbarSpacer />
    <ToolbarSection>
      <ToolbarItem>
        <button
          className="btn btn-muted btn-block"
          type="button"
          onClick={() => window.scrollTo(0, 0)}
        >
          <span className="material-icon">arrow_upward</span>
          {pgettext("go up", "Go to top")}
        </button>
      </ToolbarItem>
    </ToolbarSection>
  </Toolbar>
)

export default ThreadToolbarThird
