import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonSecondary } from "../Button"
import ViewportEvent from "../ViewportEvent"

interface ILoadMoreProps {
  data: { nextCursor: string | null } | null
  loading: boolean
  onEvent: () => void
}

const LoadMore: React.FC<ILoadMoreProps> = ({ loading, data, onEvent }) => {
  if (!data || !data.nextCursor) return null

  return (
    <ViewportEvent
      className="load-more"
      disabled={loading}
      onEnter={onEvent}
      desktopOnly
    >
      <ButtonSecondary
        loading={loading}
        text={
          loading ? (
            <Trans id="loading-more">Loading...</Trans>
          ) : (
            <Trans id="load-more">Load more</Trans>
          )
        }
        onClick={onEvent}
      />
    </ViewportEvent>
  )
}

export default LoadMore
