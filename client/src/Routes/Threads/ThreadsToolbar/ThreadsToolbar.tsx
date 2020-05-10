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
              disabled={moderation.disabled}
              icon="shield-alt"
              iconSolid
              onClick={toggle}
            />
          )}
          menu={
            <>
              <DropdownButton
                text="Open"
                icon="unlock"
                iconSolid
                onClick={moderation.openThreads}
              />
              <DropdownButton
                text="Close"
                icon="lock"
                iconSolid
                onClick={moderation.closeThreads}
              />
              <DropdownButton
                text="Move"
                icon="arrow-right"
                iconSolid
                onClick={() => {}}
              />
              <DropdownButton
                text="Delete"
                icon="times"
                iconSolid
                onClick={() => {}}
              />
              <DropdownDivider />
              {selection && (
                <DropdownButton
                  text="Clear selection"
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
