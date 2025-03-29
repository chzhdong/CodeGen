/*
 * @Author: 祝占朋 wb.zhuzhanpeng01@mesg.corp.netease.com
 * @Date: 2024-01-09 15:28:56
 * @LastEditors: Ianarua 306781523@qq.com
 * @LastEditTime: 2024-08-01 17:15:29
 * @FilePath: front_end/src/utils/utils.ts
 * @Description:
 */

import { useUser } from '@/store/useUser';
import { IChatSetting, IFileListItem, ITimeInfo, ITokenInfo } from './types';

export function addWindowsAttr(name, value) {
  window[name] = value;
}

export function getRandomString(strLen = 5) {
  const strCeils = 'abcdefghijklmnopqrstuvwxyz1234567890';
  let str = '';
  for (let i = 0; i < strLen; i += 1) {
    str = `${str}${strCeils[Math.floor(Math.random() * 36)]}`;
  }
  return str;
}

export function clearTimer(timer) {
  if (timer) {
    clearTimeout(timer);
    timer = null;
  }
}

export function isMac() {
  return /macintosh|mac os x/i.test(navigator.userAgent);
}

/**
 * 节流
 * @param {*} fn
 * @param {*} delay
 */
export const throttle = <T extends (...args: any[]) => any>(fn: T, delay: number) => {
  let timer: number | undefined;
  let last = 0;
  return function (this: ThisParameterType<T>, ...args: Parameters<T>) {
    const now = Date.now();
    if (now - last >= delay) {
      clearTimeout(timer as number);
      last = now;
      fn.apply(this, args);
    } else {
      clearTimeout(timer as number);
      timer = window.setTimeout(() => {
        fn.apply(this, args);
      }, delay);
    }
  } as T;
};

//格式化上传状态
export const getStatus = (item: IFileListItem) => {
  let str = '';
  switch (item.status) {
    case 'loading':
      str = '上传中';
      break;
    case 'red':
      if (item.errorText) {
        str = item.errorText;
      } else {
        str = '解析失败';
      }
      break;
    case 'gray':
      str = '上传成功待解析';
      break;
    case 'green':
      str = '解析成功';
      break;
    case 'yellow':
      str = '解析失败';
      break;
    default:
      break;
  }
  return str;
};

//对接口的返回值作统一处理
export const resultControl = async res => {
  return new Promise((resolve, reject) => {
    if (res?.request?.responseType === 'blob') {
      resolve(res);
    }
    if (res.errorCode === '0' || res.code === 200) {
      resolve(res.result || res.data || res);
    } else if (res.errorCode === '111') {
      const { setUserInfo } = useUser();
      setUserInfo({ token: '' });
    } else {
      reject(res);
    }
  });
};

export const formatFileSize = sizeInBytes => {
  if (sizeInBytes < 0) {
    return '未知';
  } else if (sizeInBytes < 1024) {
    return sizeInBytes + 'B';
  } else if (sizeInBytes < 1024 * 1024) {
    return (sizeInBytes / 1024).toFixed(2) + 'KB';
  } else if (sizeInBytes < 1024 * 1024 * 1024) {
    return (sizeInBytes / (1024 * 1024)).toFixed(2) + 'MB';
  } else {
    return (sizeInBytes / (1024 * 1024 * 1024)).toFixed(2) + 'G';
  }
};

export const formatDate = (timestamp, symbol = '-', timeSymbol = ':') => {
  if (!timestamp) {
    return '';
  }

  // 拆分日期和时间部分
  const datePart = timestamp.slice(0, 8); // 取前8位作为日期
  const timePart = timestamp.slice(8); // 剩余部分作为时间

  // 解析日期部分
  const year = datePart.slice(0, 4);
  const month = datePart.slice(4, 6);
  const day = datePart.slice(6, 8);

  // 检查时间部分是否存在，并解析时间
  let hour, minute;
  if (timePart) {
    hour = timePart.slice(0, 2);
    minute = timePart.slice(2, 4);
  }

  // 构建日期字符串
  let dateString = `${year}${symbol}${month}${symbol}${day}`;

  // 如果存在时间部分，添加到日期字符串
  if (timePart) {
    dateString += ` ${hour}${timeSymbol}${minute}`;
  }

  return dateString;
};

/**
 * @description 返回最近14天的日期范围
 */
export const getLastDaysRange = (days: number = 14) => {
  const today = new Date();
  const timeEnd = today.toISOString().split('T')[0]; // 获取今天的日期，格式为 'YYYY-MM-DD'

  const timeStart = new Date(today.getTime());
  timeStart.setDate(today.getDate() - days - 1); // 设置日期为今天减去days-1天
  const timeStartStr = timeStart.toISOString().split('T')[0]; // 获取14天前的日期，格式为 'YYYY-MM-DD'

  return {
    time_start: timeStartStr,
    time_end: timeEnd,
  };
};

/**
 * @description 将文件后缀和文件名分开
 * @param filePath 文件全部名称
 */
export const parseFileName = (filePath: string) => {
  const parts = filePath.split('.');
  const fileName = parts.slice(0, -1).join('.'); // 获取文件名部分
  const fileExtension = parts.at(-1); // 获取文件扩展名部分

  return {
    fileName: fileName,
    fileExtension: fileExtension,
  };
};

/**
 * @description 保存ai回答的time token信息和当前ai的模型配置
 */
export class ChatInfoClass<T = IChatSetting> {
  private timeObj: ITimeInfo;
  private tokenObj: ITokenInfo;
  private settingObj: T;
  private date: number;

  constructor() {
    this.timeObj = {
      preprocess: 0,
      condense_q_chain: 0,
      retriever_search: 0,
      web_search: 0,
      rerank: 0,
      reprocess: 0,
      llm_first_return: 0,
      first_return: 0,
      llm_completed: 0,
      chat_completed: 0,
    };
  }

  addTime(timeInfo: ITimeInfo) {
    this.timeObj = { ...this.timeObj, ...timeInfo };
  }

  addToken(tokenInfo: ITokenInfo) {
    this.tokenObj = tokenInfo;
  }

  addChatSetting(chatSettingInfo: T) {
    this.settingObj = chatSettingInfo;
  }

  addDate(date: number) {
    this.date = date;
  }

  getChatInfo() {
    return {
      timeInfo: this.timeObj,
      tokenInfo: this.tokenObj,
      settingInfo: this.settingObj,
      dateInfo: this.date,
    };
  }
}

/**
 * @description 将时间戳格式化为 2024/8/1 12:30:12 的格式
 * @param timestamp {number} 时间戳
 */
export function formatTimestamp(timestamp: number): string {
  const date = new Date(timestamp);
  const year = date.getFullYear(); // 获取年份
  const month = (date.getMonth() + 1).toString().padStart(2, '0'); // 获取月份，月份从0开始计数
  const day = date.getDate().toString().padStart(2, '0'); // 获取日
  const hours = date.getHours().toString().padStart(2, '0'); // 获取小时
  const minutes = date.getMinutes().toString().padStart(2, '0'); // 获取分钟
  const seconds = date.getSeconds().toString().padStart(2, '0'); // 获取秒

  return `${year}/${month}/${day} ${hours}:${minutes}:${seconds}`;
}

/**
 * @description 下载文件的通用函数
 * @param url URL.createObjectURL 的文件链接
 * @param fileName 下载文件的名称，如果不提供，默认为空字符串
 * @param callback 下载完成后的回调函数，如果提供了回调函数，在下载触发后执行
 */
export function downLoad(url, fileName = '', callback?) {
  let aLink = document.createElement('a');
  aLink.download = fileName;
  aLink.style.display = 'none';
  aLink.href = url;
  document.body.appendChild(aLink);
  aLink.click();
  document.body.removeChild(aLink);
  if (callback) {
    callback();
  }
}

/**
 * 从请求头中提取内容处置（Content-Disposition）字段的文件名
 * @param {Headers} headers - 请求响应头对象，包含所有响应头字段
 * @return {string} 返回解析出的文件名，如果无法解析或字段不存在，则返回空字符串
 */
export function getContentDispositionByHeader(headers: Headers): string {
  return decodeURIComponent(
    (headers['content-disposition']?.split('filename=') || [])[1].slice(1, -1) || ''
  );
}
