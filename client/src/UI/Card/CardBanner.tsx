import classNames from "classnames"
import React from "react"

interface ICardBannerProps {
  align: string
  background: string
  className?: string | null
  height: number
  url: string
  mobile?: boolean
  desktop?: boolean
}

const CardBanner: React.FC<ICardBannerProps> = ({
  align,
  background,
  className,
  height,
  url,
  mobile,
  desktop,
}) => (
  <div
    className={classNames(
      "card-banner",
      { "d-md-none": mobile, "d-none d-md-block": desktop },
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
