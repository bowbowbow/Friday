import queryString from 'query-string';
import pathToRegexp from 'path-to-regexp';
import { routerRedux } from 'dva/router';
import _ from 'lodash';
import * as chromeAPI from '../utils/chromeAPI';

export default {
  namespace: 'app',
  state: {
    power: false,
    selectors: [],
    warning: '',
  },
  subscriptions: {
    setupHistory({ dispatch, history }) {
      chromeAPI.getState().then((state) => {
        dispatch({ type: 'updateState', payload: state });
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
    * sendInitState({ payload }, { put, call, select }) {
      const app = yield select(state => state.app);
      const nextState = {
        power: app.power,
        selectors: app.selectors,
        ...payload,
      };
      yield call(chromeAPI.sendInitState, nextState);
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
