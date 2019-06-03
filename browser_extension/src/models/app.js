import queryString from 'query-string';
import pathToRegexp from 'path-to-regexp';
import { routerRedux } from 'dva/router';
import _ from 'lodash';
import * as chromeAPI from '../utils/chromeAPI';

export default {
  namespace: 'app',
  state: {
    power: false,
    keywords: [],
    warning: '',
    hideCount: {},
  },
  subscriptions: {
    setupHistory({ dispatch, history }) {
      console.log('setup!!');

      chromeAPI.getState().then((state) => {
        dispatch({ type: 'updateState', payload: state });
        dispatch({ type: 'sendInitState', payload: { state } });
      });
      chrome.runtime.onMessage.addListener(
        (request, sender, sendResponse) => {
          console.log('request :', request);
          return true; // for calling sendResponse asynchronously
        },
      );
      history.listen(({ pathname, search }) => {

      });
    },
  },
  effects: {
    * sendInitState({ payload }, { put, call }) {
      const state = payload.state;
      const res = yield call(chromeAPI.sendInitState, state);
    },
  },
  reducers: {
    updateState(state, { payload }) {
      const nextState = {
        ...state,
        ...payload,
      };
      chromeAPI.saveState(nextState);
      return nextState;
    },
  },
};
