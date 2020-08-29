import { Trans } from "@lingui/macro"
import React from "react"
import {
  ButtonDark,
  Dropdown,
  Toolbar,
  ToolbarItem,
  ToolbarSeparator,
} from "../../../UI"
import FixedContainer from "../../../UI/FixedContainer"
import { IPostsModeration } from "./ThreadPostsModeration.types"
import ThreadPostsModerationMenu from "./ThreadPostsModerationMenu"

interface IThreadPostsModerationProps {
  moderation?: IPostsModeration | null
  selection: {
    selected: Array<any>
    clear: () => void
  }
}

const ThreadPostsModeration: React.FC<IThreadPostsModerationProps> = ({
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
