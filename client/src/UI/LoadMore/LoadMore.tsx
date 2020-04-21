import React from "react"

interface ILoadMoreProps {
  loadMore: () => void
}

const LoadMore: React.FC<ILoadMoreProps> = ({ loadMore }) => (
  <button type="button" onClick={loadMore}>LOAD MOAR</button>
)

export default LoadMore