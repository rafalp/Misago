import { Trans } from "@lingui/macro"
import classnames from "classnames"
import React from "react"
import { useToastsContext } from "../../Context"
import { ButtonSecondary } from "../../UI/Button"
import { RichTextCode as RichTextCodeType } from "../../types"

interface RichTextCodeProps {
  block: RichTextCodeType
}

const RichTextCode: React.FC<RichTextCodeProps> = ({ block }) => {
  const { showToast } = useToastsContext()
  return (
    <div
      className={classnames(
        "rich-text-code",
        block.syntax ? "rich-text-code-" + block.syntax : ""
      )}
    >
      <div data-noquote="1">
        <ButtonSecondary
          icon="far fa-copy"
          text={<Trans id="rich_text.code_copy">Copy</Trans>}
          small
          onClick={(event) => {
            const code = event.currentTarget
              ?.closest("div.rich-text-code")
              ?.querySelector("pre")
            if (code) {
              navigator.clipboard.writeText(code.innerText).then(function () {
                showToast(
                  <Trans id="rich_text.code_copied">
                    Code copied to the clipboard.
                  </Trans>
                )
              })
            }
          }}
        />
      </div>
      <pre data-syntax={block.syntax || null}>
        <code dangerouslySetInnerHTML={{ __html: block.text }} />
      </pre>
    </div>
  )
}

export default RichTextCode
