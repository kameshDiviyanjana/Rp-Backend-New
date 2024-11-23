export const makerespon = ({ res, data, message,status = 200 }) => {
    const responseData = { data, message };
    if (!data) delete responseData.data;
    return res.status(status).json(responseData);
  };
  