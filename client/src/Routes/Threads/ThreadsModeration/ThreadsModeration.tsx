import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonInverse } from "../../../UI/Button"
import {
  Dropdown,
  DropdownButton,
  DropdownDivider,
} from "../../../UI/Dropdown"
import FixedContainer from "../../../UI/FixedContainer"
import { Toolbar, ToolbarItem, ToolbarSeparator } from "../../../UI/Toolbar"
import { ThreadsModerationOptions } from "../Threads.types"

interface ThreadsModerationProps {
  moderation: ThreadsModerationOptions | null
  selection: {
    selected: Array<any>
    clear: () => void
  }
}

const ThreadsModeration: React.FC<ThreadsModerationProps> = ({
  moderation,
  selection,
}) => {
  if (!moderation) return null

  return (
    <FixedContainer show={!moderation.disabled}>
      <Toolbar>
        <ToolbarSeparator />
        <ToolbarItem>
          <Dropdown
            toggle={({ ref, toggle }) => (
              <ButtonInverse
                elementRef={ref}
                loading={moderation.loading}
                text={
                  <Trans id="moderate_threads">
                    Moderate threads ({selection.selected.length})
                  </Trans>
                }
                icon="fas fa-shield-alt"
                responsive
                onClick={toggle}
              />
            )}
            menu={() => (
              <>
                {moderation.actions.map((action) => (
                  <DropdownButton
                    key={action.icon}
                    text={action.name}
                    icon={action.icon}
                    onClick={action.action}
                  />
                ))}
                <DropdownDivider />
                {selection && (
                  <DropdownButton
                    text={<Trans id="clear_selection">Clear selection</Trans>}
                    icon="far fa-square"
                    onClick={selection.clear}
                  />
                )}
              </>
            )}
          />
        </ToolbarItem>
      </Toolbar>
    </FixedContainer>
  )
}

export default ThreadsModeration
