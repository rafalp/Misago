import React from "react"
import Avatar from "../avatar"
import { UIPreviewText } from "../UIPreview"
import ThreadsListItemReadStatus from "./ThreadsListItemReadStatus"

const ThreadsListLoader = ({ showOptions }) => (
  <div className="threads-list threads-list-loader">
    <ul className="list-group">
      <li className="list-group-item threads-list-item">
        <div className="threads-list-item-col-starter">
          <Avatar size={26} />
        </div>
        {showOptions && (
          <div className="threads-list-item-col-read-status">
            <ThreadsListItemReadStatus />
          </div>
        )}
        <div className="threads-list-item-right-col">
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
            </div>
          </div>
          <div className="threads-list-item-bottom-row">
            <div className="threads-list-item-bottom-left">
              <div className="threads-list-item-col-starter-sm">
                <Avatar size={20} />
              </div>
              <div className="threads-list-item-col-category">
                <UIPreviewText width="70" />
              </div>
            </div>
            <div className="threads-list-item-bottom-right">
              <div className="threads-list-item-col-replies">
                <UIPreviewText width="50" />
              </div>
              <div className="threads-list-item-col-last-poster">
                <span className="threads-list-item-last-poster">
                  <Avatar size={26} />
                </span>
              </div>
              <div className="threads-list-item-col-last-activity">
                <span className="threads-list-item-last-activity">
                  <UIPreviewText width="50" />
                </span>
              </div>
              <div className="threads-list-item-col-last-poster-sm">
                <Avatar size={20} />
              </div>
            </div>
          </div>
        </div>
      </li>
      <li className="list-group-item threads-list-item">
        <div className="threads-list-item-col-starter">
          <Avatar size={26} />
        </div>
        {showOptions && (
          <div className="threads-list-item-col-read-status">
            <ThreadsListItemReadStatus />
          </div>
        )}
        <div className="threads-list-item-right-col">
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
            </div>
          </div>
          <div className="threads-list-item-bottom-row">
            <div className="threads-list-item-bottom-left">
              <div className="threads-list-item-col-starter-sm">
                <Avatar size={20} />
              </div>
              <div className="threads-list-item-col-category">
                <UIPreviewText width="90" />
              </div>
            </div>
            <div className="threads-list-item-bottom-right">
              <div className="threads-list-item-col-replies">
                <UIPreviewText width="70" />
              </div>
              <div className="threads-list-item-col-last-poster">
                <span className="threads-list-item-last-poster">
                  <Avatar size={26} />
                </span>
              </div>
              <div className="threads-list-item-col-last-activity">
                <span className="threads-list-item-last-activity">
                  <UIPreviewText width="40" />
                </span>
              </div>
              <div className="threads-list-item-col-last-poster-sm">
                <Avatar size={20} />
              </div>
            </div>
          </div>
        </div>
      </li>
      <li className="list-group-item threads-list-item">
        <div className="threads-list-item-col-starter">
          <Avatar size={26} />
        </div>
        {showOptions && (
          <div className="threads-list-item-col-read-status">
            <ThreadsListItemReadStatus />
          </div>
        )}
        <div className="threads-list-item-right-col">
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
            </div>
          </div>
          <div className="threads-list-item-bottom-row">
            <div className="threads-list-item-bottom-left">
              <div className="threads-list-item-col-starter-sm">
                <Avatar size={20} />
              </div>
              <div className="threads-list-item-col-category">
                <UIPreviewText width="80" />
              </div>
            </div>
            <div className="threads-list-item-bottom-right">
              <div className="threads-list-item-col-replies">
                <UIPreviewText width="50" />
              </div>
              <div className="threads-list-item-col-last-poster">
                <span className="threads-list-item-last-poster">
                  <Avatar size={26} />
                </span>
              </div>
              <div className="threads-list-item-col-last-activity">
                <span className="threads-list-item-last-activity">
                  <UIPreviewText width="45" />
                </span>
              </div>
              <div className="threads-list-item-col-last-poster-sm">
                <Avatar size={20} />
              </div>
            </div>
          </div>
        </div>
      </li>
    </ul>
  </div>
)

export default ThreadsListLoader
