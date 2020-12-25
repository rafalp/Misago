import { Plural, Trans } from "@lingui/macro"
import React from "react"
import { Button } from "../../../UI/Button"

interface ThreadsListUpdateButtonProps {
  threads: number
  disabled?: boolean
  loading?: boolean
  onClick: () => void
}

const ThreadsListUpdateButton: React.FC<ThreadsListUpdateButtonProps> = ({
  threads,
  loading,
  disabled,
  onClick,
}) => (
  <Button
    className="btn-update-threads"
    text={
      loading ? (
        <Trans id="btn.updating-threads-list">Loading threads...</Trans>
      ) : (
        <Plural
          id="btn.update-threads-list"
          value={threads}
          one="See # new or updated thread"
          other="See # new or updated threads"
        />
      )
    }
    loading={loading}
    disabled={disabled}
    onClick={onClick}
    outline
    responsive
  />
)

export default ThreadsListUpdateButton
