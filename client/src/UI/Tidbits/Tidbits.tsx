import classnames from "classnames"
import React from "react"

interface TidbitsProps {
  children?: React.ReactNode
  vertical?: boolean
}

const Tidbits: React.FC<TidbitsProps> = ({ children, vertical }) => (
  <ul
    className={classnames(
      "tidbits",
      vertical ? "list-unstyled" : "list-inline"
    )}
  >
    {children}
  </ul>
)

export default Tidbits
