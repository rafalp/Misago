import classNames from "classnames"
import React from "react"

interface ICardBannerProps {
  align: string
  background: string
  className?: string | null
  height: number
  url: string
  mobile?: boolean
}

const CardBanner: React.FC<ICardBannerProps> = ({
  align,
  background,
  className,
  height,
  url,
  mobile,
}) => (
  <div
    className={classNames(
      "card-banner",
      mobile ? "d-md-none" : "d-none d-md-block",
      className
    )}
    style={{
      height,
      backgroundColor: background,
      backgroundImage: "url(" + url + ")",
      backgroundSize: "cover",
      backgroundPositionX: align,
      backgroundPositionY: "center",
    }}
  />
)

export default CardBanner
