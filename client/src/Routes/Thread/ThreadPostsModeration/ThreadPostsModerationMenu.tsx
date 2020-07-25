import { Trans } from "@lingui/macro"
import React from "react"
import { DropdownButton, DropdownDivider } from "../../../UI"
import { IPostsModeration } from "./ThreadPostsModeration.types"

interface IThreadPostsModerationMenuProps {
  moderation: IPostsModeration
  selection: {
    selected: Array<any>
    clear: () => void
  }
}

const ThreadPostsModerationMenu: React.FC<IThreadPostsModerationMenuProps> = ({
  moderation,
  selection,
}) => (
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
)

export default ThreadPostsModerationMenu
