import { Trans } from "@lingui/macro"
import React from "react"
import { useFormContext } from "react-hook-form"
import { useFieldContext } from "../UI/Form"
import EditorBody from "./EditorBody"
import EditorButton from "./EditorButton"
import EditorControls from "./EditorControls"
import EditorMentions from "./EditorMentions"
import EditorPreview from "./EditorPreview"
import EditorPreviewButton from "./EditorPreviewButton"
import EditorTextarea from "./EditorTextarea"
import EditorToolbar from "./EditorToolbar"

interface EditorProps {
  name?: string
  disabled?: boolean
  submit?: React.ReactNode
}

const Editor: React.FC<EditorProps> = ({ name, disabled, submit }) => {
  const context = useFieldContext()
  const hookContext = useFormContext()
  const [preview, setPreview] = React.useState<string | null>(null)

  const finName = name || context.name

  const setValueInState = hookContext?.setValue
  const setValue = React.useCallback(
    (value: string) => {
      if (finName && setValueInState) setValueInState(finName, value)
    },
    [finName, setValueInState]
  )

  if (!hookContext) return null
  if (!finName) return null

  const openPreview = () => {
    const value = hookContext.getValues(finName) || ""
    if (value.trim().length > 0) {
      setPreview(value.trim())
    }
  }

  const closePreview = () => setPreview(null)

  return (
    <EditorBody disabled={disabled || context.disabled}>
      {preview && <EditorPreview markup={preview} />}
      <EditorMentions>
        <EditorTextarea
          disabled={disabled || context.disabled}
          hidden={!!preview}
          invalid={context.invalid}
          name={finName}
          register={hookContext.register}
        />
      </EditorMentions>
      <EditorToolbar>
        <div className="row">
          <EditorControls
            disabled={disabled || context.disabled || !!preview}
            setValue={setValue}
          >
            {preview ? (
              <EditorButton
                disabled={disabled || context.disabled}
                onClick={closePreview}
              >
                <Trans id="editor.write">Write</Trans>
              </EditorButton>
            ) : (
              <EditorPreviewButton
                disabled={disabled || context.disabled}
                name={finName}
                onClick={openPreview}
              />
            )}
          </EditorControls>
          <div className="col" />
          {submit && <div className="col-auto">{submit}</div>}
        </div>
      </EditorToolbar>
    </EditorBody>
  )
}

export default Editor
