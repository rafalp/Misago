import { Trans } from "@lingui/macro"
import React from "react"
import { Field } from "../../../../UI"
import { ISelectedThread } from "./ThreadsModerationSelectedThreads.types"
import ThreadsModerationSelectedThreadsButton from "./ThreadsModerationSelectedThreadsButton"
import ThreadsModerationSelectedThreadsList from "./ThreadsModerationSelectedThreadsList"

interface IThreadsModerationSelectedThreadsProps {
  threads: Array<ISelectedThread>
}

const ThreadsModerationSelectedThreads: React.FC<IThreadsModerationSelectedThreadsProps> = ({
  threads,
}) => {
  const [isOpen, setState] = React.useState<boolean>(threads.length < 3)

  return (
    <Field
      label={<Trans id="moderation.selected_threads">Selected threads</Trans>}
      input={
        <>
          <div className={isOpen ? "" : "d-none"}>
            <ThreadsModerationSelectedThreadsList threads={threads} />
          </div>
          {!isOpen && (
            <ThreadsModerationSelectedThreadsButton
              threadsCount={threads.length}
              onClick={() => setState(true)}
            />
          )}
        </>
      }
      name="threads"
    />
  )
}

export default ThreadsModerationSelectedThreads
