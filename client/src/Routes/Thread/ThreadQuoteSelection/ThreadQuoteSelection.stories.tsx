import React from "react"
import { AuthContext } from "../../../Context"
import {
  RootContainer,
  SettingsContextFactory,
  userFactory,
} from "../../../UI/Storybook"
import ThreadPost from "../ThreadPost"
import { ThreadReplyProvider, useThreadReplyContext } from "../ThreadReply"
import ThreadQuoteSelection from "."

export default {
  title: "Route/Thread/Quote Selection",
}

export const PostWithComplexMarkup = () => {
  return (
    <SettingsContextFactory>
      <AuthContext.Provider value={userFactory()}>
        <ThreadReplyProvider threadId="1">
          <RootContainer>
            <p>Text outside of quote selection.</p>
            <ThreadQuoteSelection>
              <ThreadPost
                post={{
                  id: "1",
                  richText: [
                    {
                      id: "FRAsvaGJO8",
                      type: "p",
                      text:
                        'Lorem ipsum dolor sit amet, <strong><a href="http://misago-project.org">http://misago-project.org</a></strong> adipiscing elit.',
                    },
                    {
                      id: "j9txbaKTrV",
                      type: "p",
                      text:
                        "Praesent finibus consequat eros. <strong>Phasellus ut eleifend orci.</strong> Aliquam erat volutpat. Vestibulum porttitor, sem quis mattis placerat, <em>enim neque aliquam leo</em>, id porta elit ante ut justo.",
                    },
                  ],
                  edits: 0,
                  postedAt: "2020-04-01T21:42:51Z",
                  posterName: "John",
                  poster: userFactory({ name: "John" }),
                  extra: {},
                }}
                threadId="1"
                threadSlug="test-thread"
              />
              <ThreadPost
                post={{
                  id: "2",
                  richText: [
                    {
                      id: "FRAsvaGJO8",
                      type: "h1",
                      text:
                        'Lorem ipsum dolor sit amet, <strong><a href="http://misago-project.org">http://misago-project.org</a></strong> adipiscing elit.',
                    },
                    {
                      id: "j9txbaKTrV",
                      type: "p",
                      text:
                        "Praesent finibus consequat eros. <strong>Phasellus ut eleifend orci.</strong> Aliquam erat volutpat. Vestibulum porttitor, sem quis mattis placerat, <em>enim neque aliquam leo</em>, id porta elit ante ut justo.",
                    },
                    {
                      id: "FxyMek8tGU",
                      type: "p",
                      text:
                        '<img src="https://placekitten.com/200/300" alt="Some kitten!" />',
                    },
                    {
                      id: "Ejg53h02ey",
                      type: "p",
                      text:
                        'Suspendisse enim massa, rutrum eget bibendum a, <a href="http://misago-project.org">porttitor vitae</a> turpis. Aliquam erat volutpat. Duis dapibus sapien nunc.',
                    },
                    {
                      id: "CZlWOZ5TUT",
                      type: "p",
                      text:
                        '<img src="https://placekitten.com/200/300" alt="" />',
                    },
                  ],
                  edits: 0,
                  postedAt: "2020-04-01T22:19:12Z",
                  posterName: "Aerith",
                  poster: userFactory({ name: "Aerith" }),
                  extra: {},
                }}
                threadId="1"
                threadSlug="test-thread"
              />
            </ThreadQuoteSelection>
            <p>Text outside of quote selection.</p>
            <ReplyPreview />
          </RootContainer>
        </ThreadReplyProvider>
      </AuthContext.Provider>
    </SettingsContextFactory>
  )
}

const ReplyPreview: React.FC = () => {
  const context = useThreadReplyContext()
  if (!context) return <div>MISSING THREAD REPLY CONTEXT</div>

  context.form.register("markup")
  const value = context.form.watch("markup") || ""
  return (
    <div style={{ border: "2px dashed #CCC", width: "100%", padding: "1rem" }}>
      <code>
        <pre style={{ margin: 0 }}>
          {value || <em className="text-muted">empty</em>}
        </pre>
      </code>
    </div>
  )
}
