import queryString from 'query-string';
import pathToRegexp from 'path-to-regexp';
import {routerRedux} from 'dva/router';
import {Modal, message} from 'antd';
import _ from 'lodash';
import * as chromeAPI from '../utils/chromeAPI';
import * as service from '../services/app';

export default {
  namespace: 'app',
  state: {
    power: false,
    selectors: [],
    warning: '',
    text: 'open the "https://google.com" and wait the "3 seconds".',
    code: '',
    loading: false,
  },
  subscriptions: {
    setupHistory({dispatch, history}) {
      chromeAPI.getState().then((state) => {
        state.loading = false;
        dispatch({type: 'updateState', payload: state});
      });
      chrome.runtime.onMessage.addListener(
        (request, sender, sendResponse) => {
          console.log('request :', request);
          return true; // for calling sendResponse asynchronously
        },
      );
      history.listen(({pathname, search}) => {

      });
    },
  },
  effects: {
    * sendInitState({payload}, {put, call, select}) {
      const app = yield select(state => state.app);
      const nextState = {
        power: app.power,
        selectors: app.selectors,
        ...payload,
      };
      yield call(chromeAPI.sendInitState, nextState);
    },
    * postText2Selenium({payload}, {put, call}) {
      yield put({type: 'updateState', payload: {loading: true}});
      const res = yield call(service.postText2selenium, payload);
      if (res.status === 200) {
        const data = JSON.parse(res.text);
        const code = data.code;
        if (data.error) {
          Modal.error({
            title: 'Error occurred during transforming',
            content: data.error,
          });
        } else {
          message.success('success', 2)
        }
        yield put({type: 'updateState', payload: {code, loading: false}});
      } else {
        Modal.error({
          title: 'Unknown error',
          content: 'Please contact the developer (clsrn1581@gmail.com)',
        });
        yield put({type: 'updateState', payload: {loading: false, code: ''}});
      }

    },
  },
  reducers: {
    updateState(state, {payload}) {
      const nextState = {
        ...state,
        ...payload,
      };
      chromeAPI.saveState(nextState);
      return nextState;
    },
  },
};
