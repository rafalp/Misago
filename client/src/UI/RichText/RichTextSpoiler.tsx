import { Trans } from "@lingui/macro"
import classnames from "classnames"
import React from "react"
import { RichTextSpoiler as RichTextSpoilerType } from "../../types"
import { ButtonSecondary } from "../Button"
import RichTextRenderer from "./RichTextRenderer"

interface RichTextSpoilerProps {
  block: RichTextSpoilerType
}

const RichTextSpoiler: React.FC<RichTextSpoilerProps> = ({ block }) => {
  const [revealed, setRevealed] = React.useState(false)

  return (
    <div
      className={classnames("rich-text-spoiler", {
        "rich-text-spoiler-revealed": revealed,
        "rich-text-spoiler-hidden": !revealed,
      })}
    >
      <div className="rich-text-spoiler-header" data-noquote="1">
        <Trans id="rich_text.spoiler">Hidden content</Trans>
        <ButtonSecondary
          icon={revealed ? "far fa-eye-slash" : "far fa-eye"}
          text={
            revealed ? (
              <Trans id="rich_text.spoiler_hide">Hide</Trans>
            ) : (
              <Trans id="rich_text.spoiler_reveal">Reveal</Trans>
            )
          }
          small
          onClick={() => {
            setRevealed(!revealed)
          }}
        />
      </div>
      <blockquote data-block="spoiler">
        <RichTextRenderer richText={block.children} />
      </blockquote>
    </div>
  )
}

export default RichTextSpoiler
