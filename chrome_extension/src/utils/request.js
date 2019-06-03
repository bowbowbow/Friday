import defaults from 'superagent-defaults';

const superagent = defaults();
superagent.ok(res => true);
// superagent.ok(res => res.status < 500);

const request = {
  init: () => {
    const accessToken = window.localStorage.getItem('accessToken');
    if (accessToken && accessToken !== 'undefined') {
      return superagent
      .set(
        'Authorization',
        `Token ${accessToken}`,
      )
    }
    return superagent.set(
      'Authorization',
      '',
    );
  },
  delete: url => request.init().delete(url),
  get: url => request.init().get(url),
  post: url => request.init().post(url),
  put: url => request.init().put(url),
};

export default request;
