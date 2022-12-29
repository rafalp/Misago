import React from "react"
import Avatar from "../avatar"
import { UIPreviewText } from "../UIPreview"

const ThreadsListLoader = ({ showOptions }) => (
  <div className="threads-list threads-list-loader">
    <ul className="list-group">
      <li className="list-group-item threads-list-item">
        <div className="threads-list-item-top-row">
          {showOptions && (
            <div className="threads-list-item-col-icon">
              <span className="threads-list-icon ui-preview-img"></span>
            </div>
          )}
          <div className="threads-list-item-col-title">
            <span className="threads-list-item-title">
              <UIPreviewText width="90" /> <UIPreviewText width="40" />{" "}
              <UIPreviewText width="120" />
            </span>
            <span className="threads-list-item-title-sm">
              <UIPreviewText width="90" /> <UIPreviewText width="40" />{" "}
              <UIPreviewText width="120" />
            </span>
          </div>
        </div>
        <div className="threads-list-item-bottom-row">
          <div className="threads-list-item-col-category">
            <UIPreviewText width="70" />
          </div>
          <div className="threads-list-item-col-replies">
            <UIPreviewText width="50" />
          </div>
          <div className="threads-list-item-col-last-poster">
            <span className="threads-list-item-last-poster">
              <Avatar size={32} />
            </span>
          </div>
          <div className="threads-list-item-col-last-activity">
            <span className="threads-list-item-last-activity">
              <UIPreviewText width="50" />
            </span>
          </div>
        </div>
      </li>
      <li className="list-group-item threads-list-item">
        <div className="threads-list-item-top-row">
          {showOptions && (
            <div className="threads-list-item-col-icon">
              <span className="threads-list-icon ui-preview-img"></span>
            </div>
          )}
          <div className="threads-list-item-col-title">
            <span className="threads-list-item-title">
              <UIPreviewText width="120" /> <UIPreviewText width="30" />{" "}
              <UIPreviewText width="60" />
            </span>
            <span className="threads-list-item-title-sm">
              <UIPreviewText width="120" /> <UIPreviewText width="30" />{" "}
              <UIPreviewText width="60" />
            </span>
          </div>
        </div>
        <div className="threads-list-item-bottom-row">
          <div className="threads-list-item-col-category">
            <UIPreviewText width="55" />
          </div>
          <div className="threads-list-item-col-replies">
            <UIPreviewText width="60" />
          </div>
          <div className="threads-list-item-col-last-poster">
            <span className="threads-list-item-last-poster">
              <Avatar size={32} />
            </span>
          </div>
          <div className="threads-list-item-col-last-activity">
            <span className="threads-list-item-last-activity">
              <UIPreviewText width="70" />
            </span>
          </div>
        </div>
      </li>
      <li className="list-group-item threads-list-item">
        <div className="threads-list-item-top-row">
          {showOptions && (
            <div className="threads-list-item-col-icon">
              <span className="threads-list-icon ui-preview-img"></span>
            </div>
          )}
          <div className="threads-list-item-col-title">
            <span className="threads-list-item-title">
              <UIPreviewText width="40" /> <UIPreviewText width="120" />{" "}
              <UIPreviewText width="80" />
            </span>
            <span className="threads-list-item-title-sm">
              <UIPreviewText width="40" /> <UIPreviewText width="120" />{" "}
              <UIPreviewText width="80" />
            </span>
          </div>
        </div>
        <div className="threads-list-item-bottom-row">
          <div className="threads-list-item-col-category">
            <UIPreviewText width="75" />
          </div>
          <div className="threads-list-item-col-replies">
            <UIPreviewText width="40" />
          </div>
          <div className="threads-list-item-col-last-poster">
            <span className="threads-list-item-last-poster">
              <Avatar size={32} />
            </span>
          </div>
          <div className="threads-list-item-col-last-activity">
            <span className="threads-list-item-last-activity">
              <UIPreviewText width="60" />
            </span>
          </div>
        </div>
      </li>
    </ul>
  </div>
)

export default ThreadsListLoader
