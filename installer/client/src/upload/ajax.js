function getError(action, option, xhr) {
  let msg;
  if (xhr.response) {
    msg = `${xhr.response.error || xhr.response}`;
  } else if (xhr.responseText) {
    msg = `${xhr.responseText}`;
  } else {
    msg = `fail to post ${action} ${xhr.status}`;
  }

  const err = new Error(msg);
  err.status = xhr.status;
  err.method = 'post';
  err.url = action;
  return err;
}

function getBody(xhr) {
  const text = xhr.responseText || xhr.response;
  if (!text) {
    return text;
  }

  try {
    return JSON.parse(text);
  } catch (e) {
    return text;
  }
}
export default function upload(option) {
  if (typeof XMLHttpRequest === 'undefined') {
    return;
  }
  const action = option.action // 文件上传上传路径
  const percentage = [] // 文件上传进度的数组，单项就是一个分片的进度
  //将Blob转为上传时需要的FormData格式
  const formDataList = option.chunkList.map((item, index) => {
    const formData = new FormData()
    // 额外加入组件外外面传入的data数据
    const md5 = option.chunkHashList[index]
    const chunkOption = {
      chunkSize: item.size,//当前分片大小
      chunkTotal: Math.ceil(option.file.size / option.chunkSize),// 所有切片数量
      chunkIndex: index,// 当前切片下标
      chunkHash: md5,// 当前切片hash
      fileName: option.file.name,// 文件名
      fileHash: option.fileHash,// 整个文件hash
      fileSize: option.file.size, // 总文件大小
    }
    if (option.data) {
      const data = option.data(chunkOption)
      //data是个方法，遍历data的返回值，让formData携带data中的参数
      if (data) {
        Object.keys(data).forEach(key => {
          formData.append(key, data[key])
        })
      }
    }
    formData.append(option.filename, item) // 文件的Blob
    return formData
  })

  // 更新上传进度条的方法
  const updataPercentage = (e) => {
    let loaded = 0// 当前已经上传文件的总大小
    percentage.forEach(item => {
      loaded += item
    })
    e.percent = loaded / option.file.size * 100
    option.onProgress(e)
  }
  const xhrList = [] // 所有的xhr请求
  function sendRequest(formDataList, limit) {
    let counter = 0 //上传成功的数量
    let index = 0 //当前上传文件的下标
    let isStop = false
    const len = formDataList.length
    const start = async () => {
      if (isStop) {
        return
      }
      const item = formDataList.shift()
      if (item) {
        const chunkIndex = index++
        const xhr = new XMLHttpRequest()
        // 分片上传失败回调
        xhr.onerror = function error() {
          isStop = true
          option.onError(getError(action, option, xhr))
        }
        // 分片上传成功回调
        xhr.onload = function onload() {
          if (xhr.status < 200 || xhr.status >= 300) {
            isStop = true
            option.onError(getError(action, option, xhr))
          }
          // 最后一个上传完成
          if (counter === len - 1) {
            const result = xhrList.map(item => getBody(item))
            option.onSuccess(result)
          } else {
            counter++
            start()
          }
        }
        // 上传中的时候更新进度条
        if (xhr.upload) {
          xhr.upload.onprogress = function progress(e) {
            if (e.total > 0) {
              e.percent = e.loaded / e.total * 100
            }
            percentage[chunkIndex] = e.loaded
            updataPercentage(e)
          }
        }
        xhr.open('post', action, true)
        if (option.withCredentials && 'withCredentials' in xhr) {
          xhr.withCredentials = true
        }
        const headers = option.headers || {}
        // 添加请求头
        for (const item in headers) {
          if (Object.prototype.hasOwnProperty.call(headers, item) && headers[item] !== null) {
            xhr.setRequestHeader(item, headers[item])
          }
        }
        // 文件开始上传，并把xhr对象存入xhrList中
        xhr.send(item)
        xhrList.push(xhr)
      }
    }
    while (limit > 0) {
      setTimeout(() => {
        start()
      }, Math.random() * 1000)
      limit -= 1
    }
  }

  try {
    sendRequest(formDataList, option.thread)
    return xhrList
  } catch (error) {
    option.onError(error)
  }
}
