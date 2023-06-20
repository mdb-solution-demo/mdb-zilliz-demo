let timeout: any = '';
export const delayRunFunc = ( func: Function, time: number, params?:any) => {
  if (timeout) {
    clearTimeout(timeout);
  }
  timeout = setTimeout(() => {
    params? func(params): func()
    
  }, time);
  const r = () => {
    clearTimeout(timeout);
  };
  return r;
};
