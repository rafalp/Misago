import { Plural, Trans } from "@lingui/macro"
import React from "react"
import * as Yup from "yup"
import { useBulkActionLimit } from "../../../Context"
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

  const bulkActionLimit = useBulkActionLimit()
  const DeleteThreadsSchema = Yup.object().shape({
    threads: Yup.array()
      .required("value_error.missing")
      .min(1, "value_error.list.min_items")
      .max(bulkActionLimit, "value_error.list.max_items"),
  })

  return (
    <ThreadsModerationModal
      action={ThreadsModerationModalAction.DELETE}
      title={<Trans id="moderation.delete_threads">Delete threads</Trans>}
    >
      {({ close, threads }) => (
        <>
          <ModalBody>
            <ThreadsModerationSelectedThreads
              max={bulkActionLimit}
              min={1}
              threads={threads}
            />
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
