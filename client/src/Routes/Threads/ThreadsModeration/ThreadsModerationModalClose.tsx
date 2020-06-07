import { Trans } from "@lingui/macro"
import React from "react"
import ThreadsModerationModal from "./ThreadsModerationModal"
import { ThreadsModerationModalAction } from "./ThreadsModerationModalContext"
import ThreadsModerationModalError from "./ThreadsModerationModalError"

const ThreadsModerationModalClose: React.FC = () => (
  <ThreadsModerationModal
    action={ThreadsModerationModalAction.CLOSE}
    title={<Trans id="moderation.close_threads">Close threads</Trans>}
  >
    {({ data: { threads, graphqlError, errors }, close }) => (
      <ThreadsModerationModalError
        graphqlError={graphqlError}
        errors={errors}
        threads={threads}
        close={close}
      />
    )}
  </ThreadsModerationModal>
)

export default ThreadsModerationModalClose
