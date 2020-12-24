import { Trans } from "@lingui/macro"
import React from "react"
import { useFormContext } from "react-hook-form"

interface EditorPreviewButtonProps {
  disabled?: boolean
  name: string
  onClick?: () => void
}

const EditorPreviewButton: React.FC<EditorPreviewButtonProps> = ({
  disabled,
  name,
  onClick,
}) => {
  const context = useFormContext()
  const value = context.watch<string, string>(name, "") as string
  const length = React.useMemo(() => (value || "").trim().length, [value])

  return (
    <button
      className="btn btn-outline-secondary btn-editor btn-sm"
      type="button"
      disabled={disabled || length === 0}
      onClick={onClick}
    >
      <Trans id="editor.preview">Preview</Trans>
    </button>
  )
}

export default EditorPreviewButton
