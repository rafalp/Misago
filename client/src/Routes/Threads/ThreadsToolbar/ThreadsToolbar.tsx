import { Trans } from "@lingui/macro"
import React from "react"
import {
  ButtonSecondary,
  Dropdown,
  DropdownButton,
  DropdownDivider,
  Toolbar,
  ToolbarItem,
  ToolbarSeparator,
} from "../../../UI"
import { IThreadsModeration } from "../Threads.types"
import ThreadsStartButton from "../ThreadsStartButton"

interface IThreadsToolbarProps {
  category?: {
    id: string
    slug: string
  } | null
  moderation?: IThreadsModeration | null
  selection?: {
    clear: () => void
  }
}

const ThreadsToolbar: React.FC<IThreadsToolbarProps> = ({
  category,
  moderation,
  selection,
}) => (
  <Toolbar>
    <ToolbarSeparator />
    <ToolbarItem>
      <ThreadsStartButton category={category} />
    </ToolbarItem>
    {moderation && (
      <ToolbarItem>
        <Dropdown
          toggle={({ ref, toggle }) => (
            <ButtonSecondary
              elementRef={ref}
              loading={moderation.loading}
              disabled={moderation.disabled}
              icon="shield-alt"
              iconSolid
              responsive
              onClick={toggle}
            />
          )}
          menu={
            <>
              {moderation.actions.map((action) => (
                <DropdownButton
                  key={action.icon}
                  text={action.name}
                  icon={action.icon}
                  iconSolid={action.iconSolid}
                  onClick={action.action}
                />
              ))}
              <DropdownDivider />
              {selection && (
                <DropdownButton
                  text={<Trans id="clear_selection">Clear selection</Trans>}
                  icon="square"
                  onClick={selection.clear}
                />
              )}
            </>
          }
        />
      </ToolbarItem>
    )}
  </Toolbar>
)

export default ThreadsToolbar
