import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonSecondary } from "../../../UI"

interface ILoadMoreButtonProps {
  loading: boolean
  onClick: () => void
}

const LoadMoreButton: React.FC<ILoadMoreButtonProps> = ({
  loading,
  onClick,
}) => (
  <div className="mb-5">
    <ButtonSecondary
      loading={loading}
      text={<Trans id="threads.load_more">Load more threads</Trans>}
      onClick={onClick}
    />
  </div>
)

export default LoadMoreButton
