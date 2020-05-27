import { Plural, Trans } from "@lingui/macro"
import React from "react"
import {
  ButtonPrimary,
  ButtonSecondary,
  ModalBody,
  ModalFooter,
  Spinner,
} from "../../../UI"
import ThreadsModerationModal from "./ThreadsModerationModal"
import { ThreadsModerationModalAction } from "./ThreadsModerationModalContext"
import ThreadsModerationSelectedThreads from "./ThreadsModerationSelectedThreads"

const ThreadsModerationModalDelete: React.FC = () => {
  const loading = false

  return (
    <ThreadsModerationModal
      action={ThreadsModerationModalAction.DELETE}
      title={<Trans id="moderation.delete_threads">Delete threads</Trans>}
    >
      {({ close, threads }) => (
        <>
          <ModalBody>
            <ThreadsModerationSelectedThreads threads={threads} />
          </ModalBody>
          <ModalFooter>
            <Spinner small />
            <ButtonSecondary
              text={<Trans id="cancel">Cancel</Trans>}
              disabled={loading}
              responsive
              onClick={close}
            />
            <ButtonPrimary
              text={
                <Plural
                  id="moderation.delete_threads.submit"
                  value={threads.length}
                  one="Delete # thread"
                  other="Delete # threads"
                />
              }
              disabled={loading}
              responsive
            />
          </ModalFooter>
        </>
      )}
    </ThreadsModerationModal>
  )
}

export default ThreadsModerationModalDelete
