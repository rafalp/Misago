import React from "react"
import Avatar from "misago/components/avatar"
import * as random from "misago/utils/random"

export default function () {
  return (
    <ul className="posts-list post-feed ui-preview">
      <li className="post">
        <div className="panel panel-default panel-post">
          <div className="panel-body">
            <div className="panel-content">
              <div className="post-side post-side-anonymous">
                <div className="media">
                  <div className="media-left">
                    <span>
                      <Avatar className="poster-avatar" size={50} />
                    </span>
                  </div>
                  <div className="media-body">
                    <div className="media-heading">
                      <span className="item-title">
                        <span
                          className="ui-preview-text"
                          style={{ width: random.int(30, 200) + "px" }}
                        >
                          &nbsp;
                        </span>
                      </span>
                    </div>
                    <span className="user-title user-title-anonymous">
                      <span
                        className="ui-preview-text"
                        style={{ width: random.int(30, 200) + "px" }}
                      >
                        &nbsp;
                      </span>
                    </span>
                  </div>
                </div>
              </div>
              <div className="post-heading">
                <span
                  className="ui-preview-text"
                  style={{ width: random.int(30, 200) + "px" }}
                >
                  &nbsp;
                </span>
              </div>
              <div className="post-body">
                <article className="misago-markup">
                  <p>
                    <span
                      className="ui-preview-text"
                      style={{ width: random.int(30, 200) + "px" }}
                    >
                      &nbsp;
                    </span>
                    &nbsp;
                    <span
                      className="ui-preview-text"
                      style={{ width: random.int(30, 200) + "px" }}
                    >
                      &nbsp;
                    </span>
                    &nbsp;
                    <span
                      className="ui-preview-text"
                      style={{ width: random.int(30, 200) + "px" }}
                    >
                      &nbsp;
                    </span>
                  </p>
                </article>
              </div>
            </div>
          </div>
        </div>
      </li>
    </ul>
  )
}
