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
      chromeAPI.getState().then((state) => {
        dispatch({ type: 'updateState', payload: state });
        if (state.keywords) {
          dispatch({ type: 'updateKeywords', payload: { keywords: state.keywords } });
        }
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
    * updateKeywords({ payload }, { put, call }) {
      const keywords = payload.keywords;

      yield put({ type: 'updateState', payload: { keywords } });
      const res = yield call(chromeAPI.sendKeywords, keywords);
      if (res && res.hideCount) {
        yield put({ type: 'updateState', payload: { hideCount: res.hideCount } });
      }
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
