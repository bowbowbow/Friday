import React from 'react';
import _ from 'lodash';
import {connect} from 'dva';
import Highlight from 'react-highlight'
import {Alert, Tag, Input, Button, Tooltip, Icon, Switch, Badge} from 'antd';

import styles from './app.less';

const {TextArea} = Input;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
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
            <div className={styles.title}>Test Scenario</div>
            <div className={styles.description}>Enter test scenario in text</div>
          </div>
          <div className={styles.body}>
            <TextArea rows={5}/>
            <Button className={styles.button} type="primary" icon="play-circle" block>Convert</Button>
          </div>
        </div>
        <div className={styles.section}>
          <div className={styles.header}>
            <div className={styles.title}>Selenium Code</div>
          </div>
          <div className={styles.body}>
            <Highlight language="javascript">
              {`function foo() { return 'bar' }`}
            </Highlight>
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
