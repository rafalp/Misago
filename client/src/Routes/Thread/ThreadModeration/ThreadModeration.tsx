import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonSecondary, Dropdown, DropdownButton } from "../../../UI"
import { IThreadModeration } from "../Thread.types"

interface IThreadModerationProps {
  moderation: IThreadModeration
}

const ThreadModeration: React.FC<IThreadModerationProps> = ({
  moderation,
}) => (
  <Dropdown
    toggle={({ ref, toggle }) => (
      <ButtonSecondary
        elementRef={ref}
        loading={moderation.loading}
        text={<Trans id="moderation.thread">Moderate thread</Trans>}
        icon="shield-alt"
        iconSolid
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
            iconSolid={action.iconSolid}
            disabled={action.disabled}
            onClick={action.action}
          />
        ))}
      </>
    )}
  />
)

export default ThreadModeration
