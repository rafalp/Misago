import React from "react"
import { Card, CardBanner, CardBody, CardColorBand } from "../../../UI"
import { ICategoryBanner } from "../../../types"

interface IHeaderProps {
  banner?: { full: ICategoryBanner, half: ICategoryBanner } | null
  color?: string | null
  text: React.ReactNode
}

const Header: React.FC<IHeaderProps> = ({ banner, color, text }) => (
  <Card>
    {color && <CardColorBand color={color} />}
    {banner && <CardBanner {...banner.full} desktop />}
    {banner && <CardBanner {...banner.half} mobile />}
    <CardBody>
      <h1 className="m-0">{text}</h1>
    </CardBody>
  </Card>
)

export default Header
