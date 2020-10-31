import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonSecondary } from "../../../UI/Button"
import { Dropdown, DropdownButton } from "../../../UI/Dropdown"
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
            disabled={action.disabled}
            onClick={action.action}
          />
        ))}
      </>
    )}
  />
)

export default ThreadModeration
