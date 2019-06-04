import React from 'react';
import _ from 'lodash';
import {connect} from 'dva';
import Highlight from 'react-highlight'
import {Alert, Empty, Spin, Tag, Input, Button, Tooltip, Icon, Switch, Badge} from 'antd';

import '../../node_modules/highlight.js/styles/atelier-forest-light.css'
import styles from './app.less';

const {TextArea} = Input;

const getSimpleLocation = function (href) {
  const l = document.createElement("a");
  l.href = href;
  return l.hostname.replace('www.', '') + l.pathname;
};

class App extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const {app, dispatch} = this.props;
    return (
      <div className={styles.app}>
        {app.warning ? <Alert message={app.warning} type="warning" banner closable afterClose={() => {
          dispatch({type: 'app/updateState', payload: {warning: ''}});
        }}/> : null}
        <div className={styles.title}>Friday
          <Switch
            className={styles.power}
            checked={app.power}
            onClick={(checked) => {
              dispatch({type: 'app/updateState', payload: {power: checked}});
              dispatch({type: 'app/sendInitState', payload: {power: checked}});
            }}/>
        </div>
        <div className={styles.description}>
          {app.power ? <span>Friday is currently working <Icon type="smile"/></span> :
            <span>Friday is currently not working <Icon type="meh"/></span>}
        </div>
        <div className={styles.section}>
          <div className={styles.header}>
            <div className={styles.title}>Added elements</div>
          </div>
          <div className={styles.body}>
            {app.selectors.map((selector, index) => {
              const tag = `#${selector.tagId}-${getSimpleLocation(selector.location)}`;
              const isLongTag = tag.length > 12;
              const tagText = isLongTag ? `${tag.slice(0, 12)}...` : tag;
              const tagElem = (
                <Tag key={index}
                     closable
                     afterClose={() => {
                       // const keywords = _.cloneDeep(app.keywords);
                       // _.pull(keywords, tag);
                       // dispatch({
                       //   type: 'app/updateKeywords',
                       //   payload: {
                       //     keywords,
                       //   },
                       // });
                     }}>
                  {tagText}
                </Tag>
              );
              return isLongTag ?
                <Tooltip title={`#${selector.tagId}-${selector.location}`} key={index}>{tagElem}</Tooltip> : tagElem;
            })}
          </div>
        </div>
        <div className={styles.section}>
          <div className={styles.header}>
            <div className={styles.title}>Test Scenario</div>
            <div className={styles.description}>Enter test scenario in text</div>
          </div>
          <div className={styles.body}>
            <TextArea
              rows={5}
              value={app.text}
              onChange={(e) => {
                dispatch({
                  type: 'app/updateState',
                  payload: {
                    text: e.target.value,
                  },
                });
              }}
            />
            <Button
              className={styles.button}
              type="primary"
              icon="play-circle"
              block
              onClick={() => {
                if (app.loading) return;
                dispatch({
                  type: 'app/postText2Selenium',
                  payload: {
                    text: app.text.trim(),
                    selectors: app.selectors,
                  },
                });
              }}>Transform</Button>
          </div>
        </div>
        <div className={styles.section}>
          <div className={styles.header}>
            <div className={styles.title}>Selenium Code {app.loading ? <Spin/> : null}</div>
          </div>
          <div className={styles.code}>
            {app.code ? <Highlight language="python">{app.code}</Highlight> :
              <Empty style={{marginTop: '15px'}} image={chrome.extension.getURL('img/icon-128.png')} description="Something went wrong"/>}
          </div>
        </div>
      </div>
    );
  }
}

App.propTypes = {};

function mapStateToProps(state) {
  return {
    app: state.app,
  };
}

export default connect(mapStateToProps)(App);
