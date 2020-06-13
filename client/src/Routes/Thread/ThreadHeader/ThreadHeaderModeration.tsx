import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonSecondary, Dropdown, DropdownButton } from "../../../UI"
import { IThreadModeration } from "../Thread.types"

interface IThreadHeaderModerationProps {
  editThread: () => void
  moderation: IThreadModeration
}

const ThreadHeaderModeration: React.FC<IThreadHeaderModerationProps> = ({
  editThread,
  moderation,
}) => (
  <Dropdown
    toggle={({ ref, toggle }) => (
      <ButtonSecondary
        elementRef={ref}
        loading={moderation.loading}
        icon="shield-alt"
        iconSolid
        small
        onClick={toggle}
      />
    )}
    menu={
      <>
        <DropdownButton
          text={<Trans id="moderation.edit">Edit</Trans>}
          icon="pencil-alt"
          iconSolid
          onClick={editThread}
        />
        {moderation.actions.map((action) => (
          <DropdownButton
            key={action.icon}
            text={action.name}
            icon={action.icon}
            iconSolid={action.iconSolid}
            disabled={action.disabled}
            onClick={action.action}
          />
        ))}
      </>
    }
  />
)

export default ThreadHeaderModeration
