import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonDark } from "../../../UI/Button"
import { Dropdown } from "../../../UI/Dropdown"
import { Toolbar, ToolbarItem, ToolbarSeparator } from "../../../UI/Toolbar"
import FixedContainer from "../../../UI/FixedContainer"
import { IPostsModeration } from "./ThreadPostsModeration.types"
import ThreadPostsModerationMenu from "./ThreadPostsModerationMenu"

interface ThreadPostsModerationProps {
  moderation?: IPostsModeration | null
  selection: {
    selected: Array<any>
    clear: () => void
  }
}

const ThreadPostsModeration: React.FC<ThreadPostsModerationProps> = ({
  moderation,
  selection,
}) => {
  if (!moderation) return null

  return (
    <FixedContainer show={selection.selected.length > 0}>
      <Toolbar>
        <ToolbarSeparator />
        <ToolbarItem>
          <Dropdown
            toggle={({ ref, toggle }) => (
              <ButtonDark
                elementRef={ref}
                loading={moderation.loading}
                text={
                  <Trans id="moderate_posts">
                    Moderate posts ({selection.selected.length})
                  </Trans>
                }
                icon="fas fa-shield-alt"
                small
                onClick={toggle}
              />
            )}
            menu={() => (
              <ThreadPostsModerationMenu
                moderation={moderation}
                selection={selection}
              />
            )}
          />
        </ToolbarItem>
      </Toolbar>
    </FixedContainer>
  )
}

export default ThreadPostsModeration
