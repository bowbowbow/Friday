import request from '../utils/request';
import superagent from 'superagent';

export async function postText2selenium(params) {
  return request.post(`http://143.248.134.129:8081/text2selenium`)
    .send(params)
}
