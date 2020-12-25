import { Plural } from "@lingui/macro"
import React from "react"
import { ButtonSecondary } from "../../../../UI/Button"

interface ThreadsModerationSelectedThreadsButtonProps {
  threadsCount: number
  onClick: () => void
}

const ThreadsModerationSelectedThreadsButton: React.FC<ThreadsModerationSelectedThreadsButtonProps> = ({
  threadsCount,
  onClick,
}) => (
  <ButtonSecondary
    text={
      <Plural
        id="moderation.see_selected_threads"
        value={threadsCount}
        one="See # selected thread"
        other="See # selected threads"
      />
    }
    block
    onClick={onClick}
  />
)
export default ThreadsModerationSelectedThreadsButton
