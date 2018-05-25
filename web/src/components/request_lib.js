import axios from 'axios';

export function defaultFunction () {
  console.log(`Hello, world! ${this}`);
}

let used = {}

export function makeId() {
  var text = "";
  var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

  for (var i = 0; i < 10; i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));

  if (text in used)
    text = makeId(); // possible infinite recursion
  used[text] = true;

  return text;
}

export function apiRequest (options, onOk, errors = undefined, onFail = undefined) {
  let ep = options.url;
  // options.url = 'http://localhost:5000' + options.url;
  axios(
    options
  ).then(response => {
    if (response.data['__OK__']) {
      console.log(`${ep} -- OK`);
      onOk(response.data['__PAYLOAD__']);
    } else {
      console.log(`${ep} -- FAIL`);
      if (errors) {
        errors.push({
          level : "danger",
          preface : `Endpoint ${ep}`,
          message : response.data['__DESCR__'] + " '" + response.data['__REASON__'] + "'"
        });
      }
      if (onFail !== undefined) {
        console.log("Something silly");
        onFail(response.data);
      }
    }
  }).catch(error => {
    if (error.response) {
      console.log(`${ep} -- Not 2xx`);
      if (errors)
        errors.push(
          {
            level : "danger",
            preface : `Endpoint ${ep}`,
            message : `response code ${error.response.status}`
          }
      );
    } else if (error.request) {
      console.log(`${ep} -- no answer`);
      if (errors)
        errors.push(
          {
            level : "danger",
            preface : `Endpoint ${ep}`,
            message : "no response"
          }
      );
    } else {
      console.log(`${ep} -- ${error.message}`);
      if (errors)
        errors.push(
          {
            level : "danger",
            preface : `URI ${options.url}`,
            message : error.message
          }
      );
    }
  });
}