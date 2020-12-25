import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonSecondary } from "../../../UI/Button"
import { Dropdown, DropdownButton } from "../../../UI/Dropdown"
import { ThreadModerationOptions } from "../Thread.types"

const ThreadModeration: React.FC<ThreadModerationOptions> = ({
  actions,
  loading,
}) => (
  <Dropdown
    toggle={({ ref, toggle }) => (
      <ButtonSecondary
        elementRef={ref}
        loading={loading}
        text={<Trans id="moderation.thread">Moderate thread</Trans>}
        icon="fas fa-shield-alt"
        responsive
        onClick={toggle}
      />
    )}
    menu={() => (
      <>
        {actions.map((action) => (
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
