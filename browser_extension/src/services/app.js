import request from '../utils/request';
import superagent from 'superagent';

export async function kakaoLogin(params) {
  return request.post(`/api/v1/users/kakao_login`)
  .send(params)
}

export async function getKakaoToken(params) {
  return request.post(`https://kauth.kakao.com/oauth/token`)
  .type('form')
  .send(params)
}

export async function naverLogin(params) {
  return request.post(`/api/v1/users/naver_login`)
  .send(params)
}
