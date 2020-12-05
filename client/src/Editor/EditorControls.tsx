import { t } from "@lingui/macro"
import React from "react"
import Icon from "../UI/Icon"
import EditorButton from "./EditorButton"
import {
  EditorContext,
  EditorContextProvider,
  IEditorContextValues,
} from "./EditorContext"
import {
  EditorControlCode,
  EditorControlEmoji,
  EditorControlImage,
  EditorControlLink,
  EditorControlList,
  IEditorControlProps,
} from "./EditorControl"

export interface IEditorControl {
  key: string
  title: string
  icon: string
  component?: React.ComponentType<IEditorControlProps>
  onClick?: (context: IEditorContextValues) => void
}

interface IEditorControlsProps {
  disabled?: boolean
  setValue: (value: string) => void
}

const EditorControls: React.FC<IEditorControlsProps> = ({
  disabled,
  setValue,
}) => {
  const [initialized, setInitialized] = React.useState(false)
  const textarea = React.useRef<HTMLTextAreaElement | null>(null)

  const controls: Array<IEditorControl> = [
    {
      key: "bold",
      title: t({
        id: "editor.bold",
        message: "Bolder",
      }),
      icon: "fas fa-bold",
      onClick: (context: IEditorContextValues) => {
        context.replaceSelection({
          prefix: "**",
          suffix: "**",
          default: t({
            id: "editor.bold_default",
            message: "strong text",
          }),
          trim: true,
          lstrip: /(\*|_)+$/,
          rstrip: /^(\*|_)+/,
        })
      },
    },
    {
      key: "emphasis",
      title: t({
        id: "editor.emphasis",
        message: "Emphasize",
      }),
      icon: "fas fa-italic",
      onClick: (context: IEditorContextValues) => {
        context.replaceSelection({
          prefix: "*",
          suffix: "*",
          default: t({
            id: "editor.emphasis_default",
            message: "emphasized text",
          }),
          trim: true,
          lstrip: /(\*|_)+$/,
          rstrip: /^(\*|_)+/,
        })
      },
    },
    {
      key: "strikethrough",
      title: t({
        id: "editor.strikethrough",
        message: "Strikethrough",
      }),
      icon: "fas fa-strikethrough",
      onClick: (context: IEditorContextValues) => {
        context.replaceSelection({
          prefix: "~~",
          suffix: "~~",
          default: t({
            id: "editor.strikethrough_default",
            message: "removed text",
          }),
          trim: true,
          lstrip: /~+$/,
          rstrip: /^~+/,
        })
      },
    },
    {
      key: "hr",
      title: t({
        id: "editor.hr",
        message: "Insert horizontal ruler",
      }),
      icon: "fas fa-minus",
      onClick: (context: IEditorContextValues) => {
        context.replaceSelection({
          prefix: "\n\n",
          suffix: "\n\n",
          replace: "- - -",
          lstrip: /\s+$/,
          rstrip: /^\s+/,
        })
      },
    },
    {
      key: "link",
      title: t({
        id: "editor.link",
        message: "Insert link",
      }),
      icon: "fas fa-link",
      component: EditorControlLink,
    },
    {
      key: "image",
      title: t({
        id: "editor.image",
        message: "Insert image",
      }),
      icon: "far fa-image",
      component: EditorControlImage,
    },
    {
      key: "emoji",
      title: t({
        id: "editor.emoji",
        message: "Insert emoji",
      }),
      icon: "far fa-smile",
      component: EditorControlEmoji,
    },
    {
      key: "list",
      title: t({
        id: "editor.list",
        message: "Insert list",
      }),
      icon: "fas fa-list-ul",
      component: EditorControlList,
    },
    {
      key: "quote",
      title: t({
        id: "editor.quote",
        message: "Quote",
      }),
      icon: "fas fa-quote-right",
      onClick: (context: IEditorContextValues) => {
        context.replaceSelection({
          prefix: "\n\n[quote]\n",
          suffix: "\n[/quote]\n\n",
          default: t({
            id: "editor.quote_default",
            message: "quoted text",
          }),
          trim: true,
          lstrip: /\s+$/,
          rstrip: /^\s+/,
        })
      },
    },
    {
      key: "spoiler",
      title: t({
        id: "editor.spoiler",
        message: "Spoiler",
      }),
      icon: "far fa-eye-slash",
      onClick: (context: IEditorContextValues) => {
        context.replaceSelection({
          prefix: "\n\n[spoiler]\n",
          suffix: "\n[/spoiler]\n\n",
          default: t({
            id: "editor.spoiler_default",
            message: "hidden text",
          }),
          trim: true,
          lstrip: /\s+$/,
          rstrip: /^\s+/,
        })
      },
    },
    {
      key: "code",
      title: t({
        id: "editor.code",
        message: "Insert code",
      }),
      icon: "fas fa-code",
      component: EditorControlCode,
    },
  ]

  const isDisabled = disabled || !textarea.current || !initialized

  return (
    <div
      className="col-auto editor-controls"
      ref={(element) => {
        if (element) {
          const editor = element.closest(".form-editor")
          if (editor) {
            textarea.current = editor.querySelector<HTMLTextAreaElement>(
              "textarea"
            )
            setInitialized(!!textarea.current)
          }
        }
      }}
    >
      <EditorContextProvider
        disabled={disabled || false}
        textarea={textarea.current}
        setValue={setValue}
      >
        {controls.map(
          ({ key, title, icon, component: Component, onClick }) => {
            if (Component) {
              return (
                <EditorContext.Consumer key={key}>
                  {(context) => (
                    <Component context={context} icon={icon} title={title} />
                  )}
                </EditorContext.Consumer>
              )
            }

            return (
              <EditorContext.Consumer key={key}>
                {(context) => (
                  <EditorButton
                    className={"btn-editor-" + key}
                    disabled={isDisabled}
                    title={title}
                    icon
                    onClick={() => {
                      if (onClick && !context.disabled) onClick(context)
                    }}
                  >
                    <Icon icon={icon} fixedWidth />
                  </EditorButton>
                )}
              </EditorContext.Consumer>
            )
          }
        )}
      </EditorContextProvider>
    </div>
  )
}

export default EditorControls
