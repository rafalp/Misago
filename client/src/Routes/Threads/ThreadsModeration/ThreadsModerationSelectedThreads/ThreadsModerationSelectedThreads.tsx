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
        isOpen ? (
          <ThreadsModerationSelectedThreadsList threads={threads} />
        ) : (
          <ThreadsModerationSelectedThreadsButton
            threadsCount={threads.length}
            onClick={() => setState(true)}
          />
        )
      }
    />
  )
}

export default ThreadsModerationSelectedThreads
