import { Plural, Trans } from "@lingui/macro"
import React from "react"
import { Button } from "../../../UI"

interface IThreadsListUpdateButtonProps {
  threads: number
  disabled?: boolean
  loading?: boolean
  onClick: () => void
}

const ThreadsListUpdateButton: React.FC<IThreadsListUpdateButtonProps> = ({
  threads,
  loading,
  disabled,
  onClick,
}) => (
  <Button
    className="btn-update-threads"
    text={
      loading ? (
        <Trans id="threads.list.updating">Loading threads...</Trans>
      ) : (
        <Plural
          id="threads.list.update"
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
  />
)

export default ThreadsListUpdateButton
