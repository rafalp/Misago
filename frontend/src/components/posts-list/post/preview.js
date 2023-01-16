import React from "react"
import Avatar from "misago/components/avatar"
import * as random from "misago/utils/random"

const PostPreview = () => (
  <li className="post">
    <div className="panel panel-default panel-post">
      <div className="panel-body">
        <div className="post-side post-side-registered">
          <div className="media">
            <div className="media-left">
              <span>
                <Avatar className="poster-avatar" size="100" />
              </span>
            </div>
            <div className="media-body">
              <span className="media-heading item-title">
                <span className="ui-preview-text" style={{ width: "80px" }}>
                  &nbsp;
                </span>
              </span>
              <span className="user-title user-title-anonymous">
                <span className="ui-preview-text" style={{ width: "60px" }}>
                  &nbsp;
                </span>
              </span>
            </div>
          </div>
        </div>
        <div className="panel-content">
          <div className="post-body">
            <article className="misago-markup">
              <p className="ui-preview-text" style={{ width: "100%" }}>
                &nbsp;
              </p>
              <p className="ui-preview-text" style={{ width: "70%" }}>
                &nbsp;
              </p>
              <p
                className="ui-preview-text hidden-xs hidden-sm"
                style={{ width: "85%" }}
              >
                &nbsp;
              </p>
            </article>
          </div>
        </div>
      </div>
    </div>
  </li>
)

export default PostPreview
