import queryString from 'query-string';
import pathToRegexp from 'path-to-regexp';
import {routerRedux} from 'dva/router';
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
        yield put({type: 'updateState', payload: {code}});
      } else {

      }
      yield put({type: 'updateState', payload: {loading: false}});
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
